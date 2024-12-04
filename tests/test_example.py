import sys
import os
import pytest

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.clients.service.logic import interpret_and_calculate
from itertools import combinations_with_replacement

# def test_interpret_and_calculate():
#     print("running tests")
#     data = {"23","1","1","1","1","0","1","2","2","3","2",
#     "2","3","2","1","1","1","1","1","1","0","1","1","1"
#     }
#     result = interpret_and_calculate(data)
#     print(data)

from itertools import product

# Cartesian product of [0, 1] repeated 2 times
result = list(product([0, 1], repeat=2))

# Output: [(0, 0), (0, 1), (1, 0), (1, 1)]
print(result)

result = list(combinations_with_replacement([0, 1], 2))

# Output: [(0, 0), (0, 1), (1, 1)]
print(result)

# Sample test data
data = {
    "age": "23",
    "gender": "1",
    "work_experience": "1",
    "canada_workex": "1",
    "dep_num": "0",
    "canada_born": "1",
    "citizen_status": "2",
    "level_of_schooling": "2",
    "fluent_english": "3",
    "reading_english_scale": "2",
    "speaking_english_scale": "2",
    "writing_english_scale": "3",
    "numeracy_scale": "2",
    "computer_scale": "3",
    "transportation_bool": "2",
    "caregiver_bool": "1",
    "housing": "1",
    "income_source": "5",
    "felony_bool": "1",
    "attending_school": "0",
    "currently_employed": "1",
    "substance_use": "1",
    "time_unemployed": "1",
    "need_mental_health_support_bool": "1"
}

def test_interpret_and_calculate():
    # Call the function with the sample data
    results = interpret_and_calculate(data)
    
    assert isinstance(results, dict)
    assert "baselines" in results
    assert "interventions" in results 
