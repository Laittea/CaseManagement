from typing import Dict

from fastapi import APIRouter, Response
from pydantic import BaseModel, ValidationError

from app.clients.schema import PredictionInput
from app.core.model_manager import ModelManager

# Initialize FastAPI router for ML-related endpoints
router = APIRouter(prefix="/ml", tags=["ml_models"])

# Initialize ModelManager for managing ML models
model_manager = ModelManager()


# Pydantic model to handle the model name for switching
class ModelSwitchRequest(BaseModel):
    model_name: str


@router.get("/current-model", response_model=Dict[str, str])
async def get_current_model():
    """
    Get information about the current model being used in the system.
    Returns:
        Dict containing current model information including name and version.
    """
    return {
        "current_model": model_manager.get_current_model()["current_model"],
        "model_version": "1.0.0",
        "status": "active",
        "last_updated": "2024-03-25",
    }


@router.get("/available-models", response_model=Dict[str, list])
async def get_available_models():
    """
    Get a list of available machine learning models supported by the system.
    Returns:
        Dict containing a list of model names.
    """
    try:
        models = model_manager.get_available_models()
        return {"available_models": models}
    except Exception as e:
        return {"error": f"Failed to get available models: {str(e)}"}


@router.post("/switch-model")
async def switch_model(model_request: ModelSwitchRequest, response: Response):
    """
    Switch the active machine learning model.
    Args:
        model_request: The request body containing the model name.
    Returns:
        JSON response indicating success or failure.
    """
    try:
        result, status_code = model_manager.switch_model(model_request.model_name)
    except Exception as e:
        result = {"status": "error", "message": f"Failed to switch model: {str(e)}"}
        status_code = 400
    response.status_code = status_code
    return result


@router.post("/predict")
async def predict(data: PredictionInput):
    """
    Make a prediction using the current machine learning model.
    Args:
        data (PredictionInput): The input data for prediction, validated by Pydantic schema.
    Returns:
        JSON response with the prediction result.
    """
    try:
        # Convert input data into a list of features with explicit numeric conversion
        features = [
            data.age,
            data.work_experience,
            data.canada_workex,
            int(data.level_of_schooling),  # Convert to integer
            1 if data.fluent_english.lower() == "true" else 0,  # Convert to 0/1
            data.reading_english_scale,
            data.speaking_english_scale,
            data.writing_english_scale,
            data.numeracy_scale,
            data.computer_scale,
            1 if data.transportation_bool.lower() == "true" else 0,  # Convert to 0/1
            1 if data.caregiver_bool.lower() == "true" else 0,  # Convert to 0/1
            int(data.housing),  # Convert to integer
            int(data.income_source),  # Convert to integer
            1 if data.felony_bool.lower() == "true" else 0,  # Convert to 0/1
            1 if data.attending_school.lower() == "true" else 0,  # Convert to 0/1
            1 if data.currently_employed.lower() == "true" else 0,  # Convert to 0/1
            1 if data.substance_use.lower() == "true" else 0,  # Convert to 0/1
            data.time_unemployed,
            1
            if data.need_mental_health_support_bool.lower() == "true"
            else 0,  # Convert to 0/1
        ]

        # Convert to 2D array for prediction
        model = model_manager.current_model
        prediction = model.predict(
            [features]
        )  # Make sure the input is in the expected format

        # Return the prediction as a list
        return {"prediction": prediction.tolist()}

    except ValidationError as e:
        return {"error": "Invalid input data", "details": e.errors()}
