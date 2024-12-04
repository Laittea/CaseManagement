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

from fastapi.testclient import TestClient
from app.main import app  # Replace with the correct path to your FastAPI app

client = TestClient(app)

# Sample client data
sample_data = {
    "age": "37",
    "gender": "2",
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

# 1. Test Add Client
def test_add_client():
    response = client.post("/clients/add", json=sample_data)
    if response.status_code == 200:
        data = response.json()
        print(f"Client added successfully: {data}")
        return data["client_id"]
    else:
        print(f"Failed to add client: {response.status_code}")
        return None

# 2. Test Get Client by ID
def test_get_client(client_id):
    response = client.get(f"/clients/{client_id}")
    if response.status_code == 200:
        print(f"Client fetched successfully: {response.json()}")
    else:
        print(f"Failed to fetch client: {response.status_code}")

# 3. Test Update Client
def test_update_client(client_id):
    updated_data = sample_data.copy()
    updated_data["age"] = 30  # Update some field
    response = client.put(f"/clients/update/{client_id}", json=updated_data)
    if response.status_code == 200:
        print(f"Client updated successfully: {response.json()}")
    else:
        print(f"Failed to update client: {response.status_code}")

# 4. Test Delete Client by ID
def test_delete_client(client_id):
    response = client.delete(f"/clients/delete/{client_id}")
    if response.status_code == 200:
        print(f"Client deleted successfully: {response.json()}")
    else:
        print(f"Failed to delete client: {response.status_code}")

# Running the tests
if __name__ == "__main__":
    # Test adding a client
    client_id = test_add_client()
    if client_id:
        # Test fetching the added client
        test_get_client(client_id)
        # Test updating the client
        test_update_client(client_id)
        # Test deleting the client
        test_delete_client(client_id)