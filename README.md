This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

# Documentation

## POST `/clients`

### Description
Creates a new client in the database with the provided information.

---

### Request Body

The fields for the new client must be passed as a JSON object and are encapsulated in the `ClientUpdateModel` located in `update_model.py`. All fields are optional.

| Field                          | Type    | Example                | Description                             |
|--------------------------------|---------|------------------------|-----------------------------------------|
| `age`                          | integer | `32`                  | Age of the client.                     |
| `gender`                       | string  | `"Male"`              | Gender of the client.                  |
| `work_experience`              | integer | `7`                   | Years of total work experience.        |
| `canada_workex`                | integer | `3`                   | Years of work experience in Canada.    |
| `dep_num`                      | integer | `1`                   | Number of dependents.                  |
| `canada_born`                  | string  | `"No"`                | Whether the client was born in Canada. |
| `citizen_status`               | string  | `"Citizen"`           | Citizenship status of the client.      |
| `level_of_schooling`           | string  | `"Master's degree"`   | Highest level of education completed.  |
| `fluent_english`               | string  | `"Yes"`               | Whether the client is fluent in English. |
| `reading_english_scale`        | integer | `10`                  | English reading skill level (1-10).    |
| `speaking_english_scale`       | integer | `10`                  | English speaking skill level (1-10).   |
| `writing_english_scale`        | integer | `10`                  | English writing skill level (1-10).    |
| `numeracy_scale`               | integer | `10`                  | Numeracy skill level (1-10).           |
| `computer_scale`               | integer | `10`                  | Computer skill level (1-10).           |
| `transportation_bool`          | string  | `"No"`                | Whether transportation support is needed. |
| `caregiver_bool`               | string  | `"No"`                | Whether the client is a primary caregiver. |
| `housing`                      | string  | `"Homeowner"`         | Housing status of the client.          |
| `income_source`                | string  | `"Employment"`        | Source of income.                      |
| `felony_bool`                  | string  | `"No"`                | Whether the client has a felony record. |
| `attending_school`             | string  | `"No"`                | Whether the client is currently a student. |
| `currently_employed`           | string  | `"Yes"`               | Employment status of the client.       |
| `substance_use`                | string  | `"No"`                | Whether the client has a substance use disorder. |
| `time_unemployed`              | integer | `0`                   | Time unemployed in years.              |
| `need_mental_health_support_bool` | string | `"No"`               | Whether the client needs mental health support. |
| `employment_assistance`            | integer | `1`                   | Employment assistance score (1-10).    |
| `life_stabilization`               | integer | `1`                   | Life stabilization score (1-10).       |
| `retention_services`               | integer | `1`                   | Retention services score (1-10).       |
| `specialized_services`             | integer | `1`                   | Specialized services score (1-10).     |
| `employment_related_financial_supports` | integer | `1`                | Employment-related financial support score (1-10). |
| `employer_financial_supports`      | integer | `1`                   | Employer financial support score (1-10). |
| `enhanced_referrals`               | integer | `1`                   | Enhanced referrals score (1-10).       |
| `success_rate`                     | integer | `100`                 | Client's success rate (percentage).    |

---

### Request Example

**URL:**

POST /clients

**Request Body:**

```json
{
    "age": 30,
    "gender": "Male",
    "work_experience": 5,
    "canada_workex": 3,
    "level_of_schooling": "Bachelor's",
    "fluent_english": "Yes",
    "currently_employed": "Yes"
}
```

**Responses**
**201 Created**

The client was successfully created.

**Response Example:**
```json
{
    "success": true,
    "message": "Client successfully created with ID 101",
    "client_id": "101"
}
```

**400 Bad Request**

The input data is invalid or improperly formatted.

**Response Example:**
```json
{
    "detail": "Invalid input data."
}
```

**500 Internal Server Error**

An unexpected error occurred during client creation.

**Response Example:**
```json
{
    "detail": "An error message describing the issue."
}
```

Ensure all required fields are included and properly formatted in the request body. Missing or invalid fields will result in a 400 Bad Request response.

### **PUT /clients/{client_id}**

#### **Description**
Updates specific fields of an existing client record.

---

### **Path Parameters**

| Parameter   | Type     | Description                            |
|-------------|----------|----------------------------------------|
| `client_id` | `string` | The unique ID of the client to update. |

---

### **Request Body**

The fields to be updated must be passed as a JSON object and are encapsulated in the `ClientUpdateModel` located in `update_model.py`. Unspecified fields will remain unchanged.

| Field                          | Type    | Example                | Description                             |
|--------------------------------|---------|------------------------|-----------------------------------------|
| `age`                          | integer | `32`                  | Age of the client.                     |
| `gender`                       | string  | `"Male"`              | Gender of the client.                  |
| `work_experience`              | integer | `7`                   | Years of total work experience.        |
| `canada_workex`                | integer | `3`                   | Years of work experience in Canada.    |
| `dep_num`                      | integer | `1`                   | Number of dependents.                  |
| `canada_born`                  | string  | `"No"`                | Whether the client was born in Canada. |
| `citizen_status`               | string  | `"Citizen"`           | Citizenship status of the client.      |
| `level_of_schooling`           | string  | `"Master's degree"`   | Highest level of education completed.  |
| `fluent_english`               | string  | `"Yes"`               | Whether the client is fluent in English. |
| `reading_english_scale`        | integer | `10`                  | English reading skill level (1-10).    |
| `speaking_english_scale`       | integer | `10`                  | English speaking skill level (1-10).   |
| `writing_english_scale`        | integer | `10`                  | English writing skill level (1-10).    |
| `numeracy_scale`               | integer | `10`                  | Numeracy skill level (1-10).           |
| `computer_scale`               | integer | `10`                  | Computer skill level (1-10).           |
| `transportation_bool`          | string  | `"No"`                | Whether transportation support is needed. |
| `caregiver_bool`               | string  | `"No"`                | Whether the client is a primary caregiver. |
| `housing`                      | string  | `"Homeowner"`         | Housing status of the client.          |
| `income_source`                | string  | `"Employment"`        | Source of income.                      |
| `felony_bool`                  | string  | `"No"`                | Whether the client has a felony record. |
| `attending_school`             | string  | `"No"`                | Whether the client is currently a student. |
| `currently_employed`           | string  | `"Yes"`               | Employment status of the client.       |
| `substance_use`                | string  | `"No"`                | Whether the client has a substance use disorder. |
| `time_unemployed`              | integer | `0`                   | Time unemployed in years.              |
| `need_mental_health_support_bool` | string | `"No"`               | Whether the client needs mental health support. |
| `employment_assistance`            | integer | `1`                   | Employment assistance score (1-10).    |
| `life_stabilization`               | integer | `1`                   | Life stabilization score (1-10).       |
| `retention_services`               | integer | `1`                   | Retention services score (1-10).       |
| `specialized_services`             | integer | `1`                   | Specialized services score (1-10).     |
| `employment_related_financial_supports` | integer | `1`                | Employment-related financial support score (1-10). |
| `employer_financial_supports`      | integer | `1`                   | Employer financial support score (1-10). |
| `enhanced_referrals`               | integer | `1`                   | Enhanced referrals score (1-10).       |
| `success_rate`                     | integer | `100`                 | Client's success rate (percentage).    |

---

### **Request Example**

**URL**:
PUT /clients/61


**Request Body**:
```json
{
    "age": 32,
    "work_experience": 7,
    "canada_workex": 3,
    "level_of_schooling": "Master's degree",
    "fluent_english": "Yes",
    "currently_employed": "Yes",
    "housing": "Homeowner"
}
```

**Responses**
**200 OK**

The client information was successfully updated.

**Response Example:**
```json
{
    "success": true,
    "message": "Client 61 successfully updated",
    "client_id": "61"
}
```
**404 Not Found**

No client with the specified client_id exists.

**Response Example:**
```json
{
    "detail": "Client with ID 61 not found."
}
```
**400 Bad Request**

The client_id is invalid or improperly formatted.

**Response Example:**
```json
{
    "detail": "Invalid client_id format."
}
```
**500 Internal Server Error**

An unexpected error occurred on the server.

**Response Example:**
```json
{
    "detail": "An error message describing the issue."
}
```

## DELETE `/clients/{client_id}`

### Description
Deletes a client with the specified `client_id` from the database.

### Path Parameters

| Parameter   | Type     | Description                            |
|-------------|----------|----------------------------------------|
| `client_id` | `string` | The unique ID of the client to delete. |

### Request Example

**URL:**

```
DELETE /clients/1
```

```

**404 Not Found**

No client with the specified `client_id` exists.

**Response Example:**
```json
{
    "detail": "Client with ID 1 not found."
}
```

**500 Internal Server Error**

An unexpected error occurred on the server.

**Response Example:**
```json
{
    "detail": "An error message describing the issue."
}
```

### Notes

This endpoint requires the `client_id` to be a valid **integer string**.

## GET `/clients/{client_id}`

### Description
Gets a client with the specified `client_id` from the database.

### Path Parameters

| Parameter   | Type     | Description                            |
|-------------|----------|----------------------------------------|
| `client_id` | `string` | The unique ID of the client to get. |

### Request Example

**URL:**

```
GET /clients/1
```

```

**404 Not Found**

No client with the specified `client_id` exists.

**Response Example:**
```json
{
    "detail": "Client with ID 1 not found."
}
```

**500 Internal Server Error**

An unexpected error occurred on the server.

**Response Example:**
```json
{
    "detail": "An error message describing the issue."
}
```

### Notes

This endpoint requires the `client_id` to be a valid **integer string**.


## POST `/search`

### Description
Searches for a list of clients based on the provided JSON criteria. Returns all clients that match the specified conditions.
The criteria are encapsulated in the `ClientUpdateModel` defined in `update_model.py`.
Any combination of fields can be provided in the JSON request body for filtering clients. Fields left empty will not be used as filters.

### Request Body

| Field                          | Type    | Example                | Description                             |
|--------------------------------|---------|------------------------|-----------------------------------------|
| `age`                          | integer | `32`                  | Age of the client.                     |
| `gender`                       | string  | `"Male"`              | Gender of the client.                  |
| `work_experience`              | integer | `7`                   | Years of total work experience.        |
| `canada_workex`                | integer | `3`                   | Years of work experience in Canada.    |
| `dep_num`                      | integer | `1`                   | Number of dependents.                  |
| `canada_born`                  | string  | `"No"`                | Whether the client was born in Canada. |
| `citizen_status`               | string  | `"Citizen"`           | Citizenship status of the client.      |
| `level_of_schooling`           | string  | `"Master's degree"`   | Highest level of education completed.  |
| `fluent_english`               | string  | `"Yes"`               | Whether the client is fluent in English. |
| `reading_english_scale`        | integer | `10`                  | English reading skill level (1-10).    |
| `speaking_english_scale`       | integer | `10`                  | English speaking skill level (1-10).   |
| `writing_english_scale`        | integer | `10`                  | English writing skill level (1-10).    |
| `numeracy_scale`               | integer | `10`                  | Numeracy skill level (1-10).           |
| `computer_scale`               | integer | `10`                  | Computer skill level (1-10).           |
| `transportation_bool`          | string  | `"No"`                | Whether transportation support is needed. |
| `caregiver_bool`               | string  | `"No"`                | Whether the client is a primary caregiver. |
| `housing`                      | string  | `"Homeowner"`         | Housing status of the client.          |
| `income_source`                | string  | `"Employment"`        | Source of income.                      |
| `felony_bool`                  | string  | `"No"`                | Whether the client has a felony record. |
| `attending_school`             | string  | `"No"`                | Whether the client is currently a student. |
| `currently_employed`           | string  | `"Yes"`               | Employment status of the client.       |
| `substance_use`                | string  | `"No"`                | Whether the client has a substance use disorder. |
| `time_unemployed`              | integer | `0`                   | Time unemployed in years.              |
| `need_mental_health_support_bool` | string | `"No"`               | Whether the client needs mental health support. |
| `employment_assistance`            | integer | `1`                   | Employment assistance score (1-10).    |
| `life_stabilization`               | integer | `1`                   | Life stabilization score (1-10).       |
| `retention_services`               | integer | `1`                   | Retention services score (1-10).       |
| `specialized_services`             | integer | `1`                   | Specialized services score (1-10).     |
| `employment_related_financial_supports` | integer | `1`                | Employment-related financial support score (1-10). |
| `employer_financial_supports`      | integer | `1`                   | Employer financial support score (1-10). |
| `enhanced_referrals`               | integer | `1`                   | Enhanced referrals score (1-10).       |
| `success_rate`                     | integer | `100`                 | Client's success rate (percentage).    |



### Request Example

**URL**:

POST /search


**Request Body**:
```json
{
    "age": 30,
    "housing": "None"
}

**Responses**
**200 OK**

The list of clients matching the criteria was successfully retrieved.

**Response Example:**

```json
[
    {
        "client_id": "1",
        "age": 30,
        "housing": "None",
        "work_experience": 5,
        "success_rate": 80
    },
    {
        "client_id": "2",
        "age": 30,
        "housing": "None",
        "work_experience": 6,
        "success_rate": 85
    }
]

```
**404 Not Found**

No clients matched the given criteria.

**Response Example:**
```json
{
    "detail": "No clients found matching the criteria."
}
```

**500 Internal Server Error**
An unexpected error occurred on the server.

**Response Example:**
```json
{
    "detail": "An error message describing the issue."
}
```

