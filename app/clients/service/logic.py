import numpy as np
import pickle
from itertools import product
from app.clients.schema import PredictionInput
from app.clients.util import util_get_cols
import os

column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]


current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')
model = pickle.load(open(filename, "rb"))


def convert_none_bool(value):
    """convert None to 0, True to 1, False to 0"""
    if value is None:
        return 0
    if type(value) == bool:
        return 1 if value is True else 0
    else:
        return value


def clean_input_data(data, features):
    """retrieve values from {data} following in the ORDER defined by {features}"""
    return [convert_none_bool(data.get(feat)) for feat in features]


# creates 128 possible combinations in order to run every possibility through model
def create_matrix(row):
    data = [row.copy() for _ in range(128)]
    perms = intervention_permutations(7)
    data = np.array(data)
    perms = np.array(perms)
    matrix = np.concatenate((data, perms), axis=1)
    return np.array(matrix)


# create matrix of permutations of 1 and 0 of num length
def intervention_permutations(num):
    perms = list(product([0, 1], repeat=num))
    return np.array(perms)


def get_baseline_row(row):
    print(type(row))
    base_interventions = np.array([0] * 7)  # no interventions
    row = np.array(row)
    print(row)
    print(type(row))
    line = np.concatenate((row, base_interventions))
    return line


def intervention_row_to_names(row):
    names = []
    for i, value in enumerate(row):
        if value == 1:
            names.append(column_intervention[i])
    return names


def process_results(baseline, results):
    """
    {
        baseline_probability: 80 #baseline percentage point with no interventions
        results: [
            (85, [A,B,C]) #new percentange with intervention combinations and list of intervention names
            (89, [B,C])
            (91, [D,E])
        ]
    }
    """
    result_list = []
    for row in results:
        percent = row[-1]
        names = intervention_row_to_names(row)
        result_list.append((percent, names))

    output = {
        "baseline": baseline[-1],  # if it's an array, want the value inside of the array
        "interventions": result_list,
    }
    return output


def interpret_and_calculate(data):
    raw_data = clean_input_data(data, util_get_cols())
    baseline_row = get_baseline_row(raw_data)
    baseline_row = baseline_row.reshape(1, -1)
    print("BASELINE ROW IS", baseline_row)
    intervention_rows = create_matrix(raw_data)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows)
    intervention_predictions = intervention_predictions.reshape(-1, 1)  # want shape to be a vertical column, not a row
    result_matrix = np.concatenate((intervention_rows, intervention_predictions), axis=1)  # CHANGED AXIS

    # sort this matrix based on prediction
    # print("RESULT SAMPLE::", result_matrix[:5])
    result_order = result_matrix[:, -1].argsort()  # take all rows and only last column, gives back list of indexes sorted
    result_matrix = result_matrix[result_order]  # indexing the matrix by the order

    # slice matrix to only top N results
    result_matrix = result_matrix[-3:, -8:]  # -8 for interventions and prediction, want top 3, 3 combinations of intervention
    # post process results if needed ie make list of names for each row
    results = process_results(baseline_prediction, result_matrix)
    # build output dict
    print(f"RESULTS: {results}")
    return results


# raw data from front end
test_model = {
    "age": "18",
    "gender": "M",
    "work_experience": "3",
    "canada_workex": 0,
    "dep_num": "1",
    "canada_born": "true",
    "citizen_status": "citizen",
    "level_of_schooling": "Grade 12 or equivalent",
    "fluent_english": "true",
    "reading_english_scale": "3",
    "speaking_english_scale": "1",
    "writing_english_scale": "3",
    "numeracy_scale": 0,
    "computer_scale": "2",
    "transportation_bool": "false",
    "caregiver_bool": "true",
    "housing": "Living with family/friend",
    "income_source": "No Source of Income",
    "felony_bool": "true",
    "attending_school": "false",
    "currently_employed": "true",
    "substance_use": "true",
    "time_unemployed": "1",
    "need_mental_health_support_bool": "false"
}

# the converted data
test_converted = {'age': 18, 'gender': 1, 'work_experience': 3, 'canada_workex': 0, 'dep_num': 1, 'canada_born': True,
                  'citizen_status': 0, 'level_of_schooling': 5, 'fluent_english': True, 'reading_english_scale': 3,
                  'speaking_english_scale': 1, 'writing_english_scale': 3, 'numeracy_scale': 0, 'computer_scale': 2,
                  'transportation_bool': False, 'caregiver_bool': True, 'housing': 5, 'income_source': 1,
                  'felony_bool': True, 'attending_school': False, 'currently_employed': True, 'substance_use': True,
                  'time_unemployed': 1, 'need_mental_health_support_bool': False}

# output after data converting
test_output = [18, 1, 3, 0, 1, 1, 0, 5, 1, 3, 1, 3, 0, 2, 0, 1, 5, 1, 1, 0, 1, 1, 1, 0]

# prediction result
test_prediction_result = {
    "baseline": 67.6,
    "interventions": [
        (68.7, ["Life Stabilization", "General Employment Assistance Services", "Specialized Services", "Employment-Related Financial Supports for Job Seekers and Employers"]),
        (68.7, ["Life Stabilization", "Specialized Services", "Employment-Related Financial Supports for Job Seekers and Employers"]),
        (69.0, ["Life Stabilization", "Specialized Services"])]
}

# ordered features for test
test_features = ['age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
                      'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
                      'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool',
                      'caregiver_bool', 'housing', 'income_source', 'felony_bool', 'attending_school',
                      'currently_employed', 'substance_use', 'time_unemployed', 'need_mental_health_support_bool']


def get_data():
    return PredictionInput(**test_model).model_dump(by_alias=True)


def test_dump_model():
    """test to check the dumped model"""
    print("\n#################### test_dump_model() ####################")
    refactor_converted = get_data()
    if refactor_converted == test_converted:
        print("PASS\n")
    else:
        print("FAIL\n")


def test_clean_input_data():
    """test data type conversion"""
    print("\n#################### test_clean_input_data() ####################")
    data = get_data()
    refactor_output = clean_input_data(data, test_features)

    if len(test_output) != len(refactor_output):
        print("FAIL: len not equals\n")
        return

    for i in range(len(test_output)):
        if test_output[i] != refactor_output[i]:
            print("FAIL: the {} th element not equals. origin:{}, refactor:{}\n".format(i, test_output[i],
                                                                                        refactor_output[i]))
            return
    print("PASS\n")


def test_prediction():
    """test the whole prediction process"""
    print("\n#################### test_prediction() ####################")
    data = get_data()
    result = interpret_and_calculate(data)
    if result == test_prediction_result:
        print("PASS\n")
    else:
        print("FAIL\n")
