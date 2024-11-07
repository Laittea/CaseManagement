from typing import List
import pandas as pd
import json
import numpy as np
import pickle
from itertools import combinations_with_replacement
from itertools import product
from pydantic import BaseModel
from app.clients.schema import PredictionInput

column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]

# loads the model into logic

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')
model = pickle.load(open(filename, "rb"))


def convert_none_bool(value):
    """
    convert None to 0, True to 1, False to 0
    """
    if value is None:
        return 0
    if type(value) == bool:
        return 1 if value is True else 0
    else:
        return value


def clean_input_data(data):
    # TODO: keep the field order the same as in model.py by reading a config file
    output = [convert_none_bool(v) for v in data.values()]
    return output


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
    ##Example:
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
    raw_data = clean_input_data(data)
    baseline_row = get_baseline_row(raw_data)
    baseline_row = baseline_row.reshape(1, -1)
    print("BASELINE ROW IS", baseline_row)
    intervention_rows = create_matrix(raw_data)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows)
    intervention_predictions = intervention_predictions.reshape(-1, 1)  # want shape to be a vertical column, not a row
    result_matrix = np.concatenate((intervention_rows, intervention_predictions), axis=1)  ##CHANGED AXIS

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


#################### Test Data and Methods ####################

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

# validated dict data for test (unconverted)
test_data = {'age': 18, 'gender': 1, 'work_experience': 3, 'canada_workex': 0, 'dep_num': 1, 'canada_born': 1,
             'citizen_status': 0, 'level_of_schooling': 'Grade 12 or equivalent', 'fluent_english': 'true',
             'reading_english_scale': 3, 'speaking_english_scale': 1, 'writing_english_scale': 3, 'numeracy_scale': 0,
             'computer_scale': 2, 'transportation_bool': 'false', 'caregiver_bool': 'true',
             'housing': 'Living with family/friend', 'income_source': 'No Source of Income', 'felony_bool': 'true',
             'attending_school': 'false', 'currently_employed': 'true', 'substance_use': 'true', 'time_unemployed': 1,
             'need_mental_health_support_bool': 'false'}

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


def test_data_type_conversion():
    """test the conversion of diff data types"""
    print("\n#################### test_data_type_conversion() ####################")
    model_refactor = PredictionInput(**test_model)
    output_refactor = model_refactor.model_dump(by_alias=True)
    output_refactor = [v for v in output_refactor.values()]

    if len(test_output) != len(output_refactor):
        print("FAIL: len not equals\n")
        return

    for i in range(len(test_output)):
        if test_output[i] != output_refactor[i]:
            print("FAIL: the {} th element not equals. origin:{}, refactor:{}\n".format(i, test_output[i], output_refactor[i]))
            return
    print("PASS\n")


def test_prediction():
    """test the whole prediction process"""
    print("\n#################### test_prediction() ####################")
    model_refactor = PredictionInput(**test_model)
    output_refactor = model_refactor.model_dump(by_alias=True)
    result = interpret_and_calculate(output_refactor)
    # print(result)
    if result == test_prediction_result:
        print("PASS\n")
    else:
        print("FAIL\n")

