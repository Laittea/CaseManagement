
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.clients.service.create import create_client
from app.clients.service.logic import interpret_and_calculate
from app.clients.service.delete import delete_client
from app.clients.schema import PredictionInput
from app.clients.service.retrieve import retrieve_client, search_clients

from app.clients.service.update import update_client
from app.clients.service.update_model import ClientUpdateModel
from fastapi import Body


router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.delete("/{client_id}")
async def delete_client_endpoint(client_id: str):
    print(f"Delete client: {client_id}")
    return await delete_client(client_id)

@router.put("/{client_id}")
async def update_client_endpoint(client_id: str, update_data: ClientUpdateModel = Body(...)):
    print(f"Update client: {client_id}")
    return await update_client(client_id, update_data)

@router.get("/{client_id}")
async def query_client(client_id: str):
    print(f"Query client: {client_id}")
    client_data = await retrieve_client(client_id)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found")
    return client_data

@router.post("/")
async def create_client_endpoint(client_data: ClientUpdateModel = Body(...)):
    print("Create new client")
    return await create_client(client_data)

@router.post("/search")
async def search_clients_endpoint(criteria: ClientUpdateModel = Body(...)):
    print("Search clients with given info")
    return await search_clients(criteria)
