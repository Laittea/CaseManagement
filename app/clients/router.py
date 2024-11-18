from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

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
