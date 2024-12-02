import numpy as np
import pickle
from itertools import product
from app.clients.schema import PredictionInput
from app.clients.util import util_get_cols
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from .env
MODEL_TYPE = os.getenv("MODEL_TYPE", "RandomForestRegressor")  # Default: RandomForestRegressor
MODEL_OUTPUT_NAME = os.getenv("MODEL_OUTPUT_NAME", "random_forest_model.pkl")  # Default: different.pkl

# Dynamically load the model
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, MODEL_OUTPUT_NAME)
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
    print(f"Model of type {MODEL_TYPE} loaded successfully from {model_path}")
except FileNotFoundError:
    print(f"Error: Model file not found at {model_path}. Please check the MODEL_OUTPUT_NAME in .env.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")


column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]


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
    print("ML MODEL IS", MODEL_TYPE)
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
