"""
This module contains original router info
"""

from fastapi import APIRouter
# from fastapi.responses import HTMLResponse

from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    """
    Handles the prediction request, processes the input data, and returns the calculated result.

    Args:
        data (PredictionInput): The input data for the prediction.

    Returns:
        The result of the prediction from the interpret_and_calculate function.
    """
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())
