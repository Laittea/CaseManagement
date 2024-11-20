# SPRINT 3: Project Progress Summary

## Overview
In Sprint 3, we focused on testing, enhancing, and documenting the core functionality of our database service project for frontend engineers. The sprint objectives included ensuring seamless database connectivity, improving user experience by handling edge cases, adding robust tests, and creating a user guide tailored to our target audience.

## Accomplishments

### 1. Testing Database Connectivity
We validated the connection between the application and the MySQL database to ensure reliability:
- Confirmed that the application could create, update, retrieve, and delete data from the database without errors.
- Addressed initial connection challenges by refining configurations for the connection pool.
### 2. All CRUD API EndPoints Implemented
We implemented all api endpoints: 
-   GET: clients/ --> get all clients
-   GET: clients/{id} --> get client by id
-    POST: clients/ --> Insert a new client with proper body
-    UPDATE: clients/{id} --> Update Client information with partial body
  -  DELETE: clients/{id} --> Delete Record by id from the database
### 3. Adjusting Database Design
We restructured the database to improve efficiency and support future scalability:
- Adjusted database field types to better align with data requirements, optimizing storage and query performance.
- Defined a new **primary tree** structure to enhance data organization and retrieval. This adjustment allows for a more logical and hierarchical representation of related entities in the database.
- Updated documentation to reflect the new database design, ensuring compatibility with frontend engineers’ needs.

### 4. Running the Project for Database Operations
Documented the steps to set up the project and interact with the database, ensuring smooth onboarding for developers:
- Verified that all endpoints worked correctly for editing and retrieving database content.
- Ensured developers could replicate the process in their local environments.

**Example of Running the Project:**

# Set up virtual environment and install dependencies
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload

### 4. Adding Edge Cases
We expanded functionality to handle uncommon user scenarios and improve overall robustness:
- Implemented input validation to manage invalid or missing data.
- Enhanced error handling with detailed, user-friendly error messages.
- In Sprint 3, we made our database service more reliable and easier to use. The API now handles problems like missing or incomplete client data by showing clear error messages instead of crashing. For example, if the age field is missing in a request, the API will respond with a message explaining the issue. We also tested all the endpoints thoroughly to make sure they work well. Additionally, we created a user guide to help frontend engineers set up and use the service easily. These improvements prepare us well for the next steps in the project.

### 5. Writing and Running Tests
We developed and executed tests to ensure the reliability of the database operations:
Created unit and integration tests for the following API endpoints:
- POST to add new client data.
- GET to retrieve client information by ID.
- PUT to update existing client records.
- DELETE to remove client records.
Verified edge case handling through additional test cases.
Ensured the tests passed successfully, confirming system stability.
**Example Test Structure:** 
def test_get_client():
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

### 6. Writing a User Guide
We created a user guide tailored to frontend engineers, outlining:
- Steps to set up the project environment.
- Instructions for using the API endpoints.
- Guidance on handling common errors and testing the endpoints.
- Ensured the guide is clear and easy to follow for our target market.

## Next Steps
- Increase Test Coverage
Add more test cases for the same endpoint to validate handling of different scenarios, ensuring robustness and consistency.
- Update Edge Case Handling
Implement logic to handle consecutive identical POST requests gracefully, avoiding redundant entries or unexpected errors.
Add functionality to provide a clear and informative response when a user attempts to delete a non-existent account.
- Refactor and Optimize Code Structure
Adjust the project environment by transferring part of the codebase into router.py to improve modularity and maintainability.

## Conclusion
Sprint 3 has strengthened the foundation of our project by ensuring database connectivity, addressing edge cases, adding comprehensive tests, and documenting the process for frontend engineers. This progress positions us well for further enhancements in upcoming sprints.
