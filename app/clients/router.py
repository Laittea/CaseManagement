from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.clients.service.logic import interpret_and_calculate
from app.clients.service.delete import delete_client
from app.clients.schema import PredictionInput

from fastapi import HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from app.clients.service.update import update_client_data, ClientUpdateRequest
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


@router.put("/client/{client_id}")
async def update_client(client_id: int, update_data: ClientUpdateRequest, db: Session = Depends(get_db)):
    try:
        updated_client = update_client_data(client_id, update_data.dict(exclude_unset=True), db)
        return updated_client
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))