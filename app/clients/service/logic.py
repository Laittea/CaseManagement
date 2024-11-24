"""
Logic for processing user data and calculating interventions.
Uses a trained model to predict outcomes based on user input.
"""

import os
import pickle
from itertools import product

try:
    import numpy as np  # Ensure numpy is installed via `pip install numpy`
except ImportError as e:
    raise ImportError("numpy is required but not installed. Install it using `pip install numpy`.") from e

# Columns representing possible interventions
column_intervention = [
    'Life Stabilization',
    'General Employment Assistance Services',
    'Retention Services',
    'Specialized Services',
    'Employment-Related Financial Supports for Job Seekers and Employers',
    'Employer Financial Supports',
    'Enhanced Referrals for Skills Development'
]

# Load the trained model
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, 'model.pkl')
with open(filename, "rb") as file:
    model = pickle.load(file)


def clean_input_data(data):
    """
    Translate input data into the format required by the trained model.
    Args:
        data (dict): Input data from the frontend.
    Returns:
        list: Transformed numerical data in a specific order.
    """
    columns = [
        "age", "gender", "work_experience", "canada_workex", "dep_num", "canada_born",
        "citizen_status", "level_of_schooling", "fluent_english", "reading_english_scale",
        "speaking_english_scale", "writing_english_scale", "numeracy_scale", "computer_scale",
        "transportation_bool", "caregiver_bool", "housing", "income_source", "felony_bool",
        "attending_school", "currently_employed", "substance_use", "time_unemployed",
        "need_mental_health_support_bool"
    ]
    demographics = {key: data[key] for key in columns if key in data}
    output = []
    for column in columns:
        value = demographics.get(column, None)
        if isinstance(value, str):
            value = convert_text(value)
        output.append(value)
    return output


def convert_text(data):
    """
    Convert textual data from the frontend into numerical values.
    Args:
        data (str): The data to convert.
    Returns:
        int: Converted numerical value.
    """
    categorical_cols_integers = [
        {"": 0, "true": 1, "false": 0, "no": 0, "yes": 1},
        {
            'Grade 0-8': 1, 'Grade 9': 2, 'Grade 12 or equivalent': 5,
            'Bachelor’s degree': 13, 'Post graduate': 14
        },
        {
            'Renting-private': 1, 'Homeowner': 4, 'Homeless or transient': 9
        },
        {
            'No Source of Income': 1, 'Employment': 8, 'Self-Employment': 9
        }
    ]
    for category in categorical_cols_integers:
        if data in category:
            return category[data]
    return int(data) if isinstance(data, str) and data.isnumeric() else data


def create_matrix(row):
    """
    Create a matrix with all possible combinations of interventions.
    Args:
        row (list): Baseline data row.
    Returns:
        numpy.ndarray: Matrix of permutations with baseline data.
    """
    data = [row.copy() for _ in range(128)]
    perms = intervention_permutations(7)
    return np.concatenate((data, perms), axis=1)


def intervention_permutations(num):
    """
    Generate all permutations of 0s and 1s for the given length.
    Args:
        num (int): Length of the permutation.
    Returns:
        numpy.ndarray: Array of permutations.
    """
    return np.array(list(product([0, 1], repeat=num)))


def get_baseline_row(row):
    """
    Create a baseline row with no interventions applied.
    Args:
        row (list): Input data row.
    Returns:
        numpy.ndarray: Baseline row with no interventions.
    """
    base_interventions = np.array([0] * 7)
    return np.concatenate((row, base_interventions))


def intervention_row_to_names(row):
    """
    Map intervention flags to their corresponding names.
    Args:
        row (list): Row with intervention flags.
    Returns:
        list: Names of interventions applied.
    """
    return [column_intervention[i] for i, value in enumerate(row) if value == 1]


def process_results(baseline, predictions):
    """
    Process results and map them to a structured output.
    Args:
        baseline (numpy.ndarray): Baseline prediction.
        predictions (numpy.ndarray): Prediction results with interventions.
    Returns:
        dict: Processed results with baseline and intervention details.
    """
    result_list = [(row[-1], intervention_row_to_names(row[:-1])) for row in predictions]
    return {
        "baseline": baseline[-1],
        "interventions": result_list,
    }


def interpret_and_calculate(data):
    """
    Clean input data, generate predictions, and process results.
    Args:
        data (dict): Raw input data.
    Returns:
        dict: Processed prediction results.
    """
    raw_data = clean_input_data(data)
    baseline_row = get_baseline_row(raw_data).reshape(1, -1)
    intervention_rows = create_matrix(raw_data)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows).reshape(-1, 1)
    result_matrix = np.concatenate((intervention_rows, intervention_predictions), axis=1)
    result_matrix = result_matrix[result_matrix[:, -1].argsort()][-3:, -8:]
    return process_results(baseline_prediction, result_matrix)


if __name__ == "__main__":
    print("Running predictions...")
    sample_data = {
        "age": "23", "gender": "1", "work_experience": "1", "canada_workex": "1", "dep_num": "0",
        "canada_born": "1", "citizen_status": "2", "level_of_schooling": "2", "fluent_english": "3",
        "reading_english_scale": "2", "speaking_english_scale": "2", "writing_english_scale": "3",
        "numeracy_scale": "2", "computer_scale": "3", "transportation_bool": "2", "caregiver_bool": "1",
        "housing": "1", "income_source": "5", "felony_bool": "1", "attending_school": "0",
        "currently_employed": "1", "substance_use": "1", "time_unemployed": "1",
        "need_mental_health_support_bool": "1"
    }
    results = interpret_and_calculate(sample_data)
    print(results)
