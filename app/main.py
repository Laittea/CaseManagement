"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from app.models import Base, User, UserRole, Client, ClientCase
from app.database import engine
from app.clients.router import router as clients_router
from app.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from pydantic import BaseModel
from app.core.model_manager import ModelManager  # Import the model manager
from app.clients.schema import PredictionInput  # Import the schema
from pydantic import ValidationError
from fastapi.responses import HTMLResponse

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Case Management API",
    description="API for managing client cases",
    version="1.0.0",
)

# Include routers
app.include_router(auth_router)
app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)

# Initialize ModelManager for managing ML models
model_manager = ModelManager()


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint that provides a welcome message and links to the API documentation.
    """
    return """
    <html>
        <head>
            <title>Case Management API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 { color: #2c3e50; }
                .links {
                    margin-top: 20px;
                }
                .links a {
                    display: inline-block;
                    margin-right: 20px;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
                .links a:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to Case Management API</h1>
            <p>This is the root endpoint of the Case Management API. Please use the following links to access the API documentation:</p>
            <div class="links">
                <a href="/docs">Swagger UI Documentation</a>
                <a href="/redoc">ReDoc Documentation</a>
            </div>
        </body>
    </html>
    """


# Pydantic model to handle the model name for switching
class ModelSwitchRequest(BaseModel):
    model_name: str


@app.get("/api/current-model", response_model=Dict[str, str])
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


@app.get("/api/available-models", response_model=Dict[str, list])
async def get_available_models():
    """
    Get a list of available machine learning models supported by the system.
    Returns:
        Dict containing a list of model names.
    """
    return model_manager.get_available_models()


@app.post("/api/switch-model")
async def switch_model(model_request: ModelSwitchRequest):
    """
    Switch the active machine learning model.
    Args:
        model_request: The request body containing the model name.
    Returns:
        JSON response indicating success or failure.
    """
    result = model_manager.switch_model(model_request.model_name)
    return result


@app.post("/predict")
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
