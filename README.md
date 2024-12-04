This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

## Assessment Tool Documentation

This API provides several endpoints to handle client-related operations, such as predicting outcomes based on input data, adding client information to an SQLite database, retrieving client information, updating client data, and deleting a client from the database.

### Prerequisites
To run this project, ensure that the following tools are installed on your system:

* Python 3.8 or later
* FastAPI
* SQLite

### API Endpoints
1. POST /clients/predictions  
This endpoint accepts input data and returns a prediction result by calling the interpret_and_calculate logic.

Request:
* Method: POST
* URL: /clients/predictions

2. POST /clients/add  
This endpoint adds the input data to the SQLite database and returns the newly created client_id along with the prediction result.

Request:
* Method: POST
* URL: /clients/add
* Body: Same as /clients/predictions

3. GET /clients/{client_id}  
This endpoint retrieves a client's information by client_id from the database.

Request:
* Method: GET
* URL: /clients/{client_id}

4. PUT /clients/update/{client_id}  
This endpoint updates the client information for the provided client_id using the input data.

Request:

* Method: PUT
* URL: /clients/update/{client_id}
* Body: Same as /clients/predictions

5. DELETE /clients/delete/{client_id}  
This endpoint deletes the client record from the database using the provided client_id.

Request:
* Method: DELETE
* URL: /clients/delete/{client_id}

### Database Configuration
This project uses an SQLite database to store client information. The database schema can be defined as follows:

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    gender TEXT,
    work_experience INTEGER,
    canada_workex INTEGER,
    dep_num INTEGER,
    canada_born BOOLEAN,
    citizen_status TEXT,
    level_of_schooling TEXT,
    fluent_english BOOLEAN,
    reading_english_scale INTEGER,
    speaking_english_scale INTEGER,
    writing_english_scale INTEGER,
    numeracy_scale INTEGER,
    computer_scale INTEGER,
    transportation_bool BOOLEAN,
    caregiver_bool BOOLEAN,
    housing TEXT,
    income_source TEXT,
    felony_bool BOOLEAN,
    attending_school BOOLEAN,
    currently_employed BOOLEAN,
    substance_use TEXT,
    time_unemployed INTEGER,
    need_mental_health_support_bool BOOLEAN
);

You can create the database by running this SQL command on your SQLite database engine.