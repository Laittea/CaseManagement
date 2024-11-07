from fastapi import APIRouter
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput


router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump(by_alias=True))
    return interpret_and_calculate(data.model_dump(by_alias=True))
