from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List

from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput, Client, ClientUpdate

from app.database import clients_collection
from bson import ObjectId

from datetime import datetime, date

router = APIRouter(prefix="/clients", tags=["clients"])

mock_clients_db = {
    1: Client(
        id="1",
        first_name="Amy",
        last_name="Doe",
        email="amy.doe@example.com",
        date_of_birth="1995-04-23",
        address="123 Main St, Springfield",
        phone="123-456-7890"
    ),
    2: Client(
        id="2",
        first_name="Bob",
        last_name="Smith",
        email="bob.smith@example.com",
        date_of_birth="1999-08-17",
        address="456 Elm St, Springfield",
        phone="098-765-4321"
    ),
}

def generate_new_id():
    return max(mock_clients_db.keys(), default=0) + 1


@router.post("/create", response_model=Client, summary="Create a new client")
async def create_client(client_data: Client):
    client_dict = client_data.dict(exclude={"id"})
    
    # Convert any `datetime.date` fields to `datetime.datetime`
    for key, value in client_dict.items():
        if isinstance(value, date):
            client_dict[key] = datetime.combine(value, datetime.min.time())
    
    result = await clients_collection.insert_one(client_dict)
    client_dict["_id"] = result.inserted_id
    return Client(id=str(client_dict["_id"]), **client_dict)


@router.get("/clients/{id}", response_model=Client, summary="Retrieve client by ID")
async def get_client_by_id(id: str):
    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    # Convert ObjectId to string and return a formatted client object
    client["id"] = str(client["_id"])
    del client["_id"]
    return client


@router.get("/clients", response_model=List[Client], summary="Retrieve all clients")
async def get_all_clients():
    clients_cursor = await clients_collection.find().to_list(length=100)
    # Convert _id to id and return the list
    for client in clients_cursor:
        client["id"] = str(client["_id"])
        del client["_id"]

    return clients_cursor


@router.delete("/clients/{id}", response_model=None, summary="Delete client by ID")
async def delete_client_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    delete_result = await clients_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return {"message": f"Client with ID {id} deleted successfully."}


@router.delete("/clients", response_model=None, summary="Delete all clients")
async def delete_all_clients():
    await clients_collection.delete_many({})
    return {"message": "All clients deleted successfully."}


@router.put("/clients/{id}", response_model=Client, summary="Update client by ID")
async def update_client(id: str, client_data: ClientUpdate):
    client = await clients_collection.find_one({"_id": ObjectId(id)})
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    # Convert datetime.date to datetime.datetime for fields that are datetime.date
    updated_fields = client_data.dict(exclude_unset=True)
    # Ensure that any datetime.date objects are converted to datetime.datetime
    for field, value in updated_fields.items():
        if isinstance(value, date):
            updated_fields[field] = datetime.combine(value, datetime.min.time())

    await clients_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_fields})

    updated_client = await clients_collection.find_one({"_id": ObjectId(id)})
    updated_client["id"] = str(updated_client["_id"])
    del updated_client["_id"]

    return updated_client