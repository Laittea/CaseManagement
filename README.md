This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

# Documentation

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
## Responses

**200 OK**

The client was successfully deleted.

**Response Example:**
```json
{
    "success": true,
    "message": "Client 1 successfully deleted",
    "client_id": "1"
}
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
