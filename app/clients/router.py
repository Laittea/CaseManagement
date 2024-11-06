from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List

from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput, Client

router = APIRouter(prefix="/clients", tags=["clients"])

mock_clients_db = {
    1: Client(
        id=1,
        first_name="Amy",
        last_name="Doe",
        email="amy.doe@example.com",
        date_of_birth="1995-04-23",
        address="123 Main St, Springfield",
        phone="123-456-7890"
    ),
    2: Client(
        id=2,
        first_name="Bob",
        last_name="Smith",
        email="bob.smith@example.com",
        date_of_birth="1999-08-17",
        address="456 Elm St, Springfield",
        phone="098-765-4321"
    ),
}

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.get("/clients/{id}", response_model=Client, summary="Retrieve client by ID")
async def get_client_by_id(id: int):
    client = mock_clients_db.get(id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/clients", response_model=List[Client], summary="Retrieve all clients")
async def get_all_clients():
    return list(mock_clients_db.values())
