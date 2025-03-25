"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from app import models
from app.database import engine
from app.clients.router import router as clients_router
from app.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

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

@app.get("/api/current-model", response_model=Dict[str, str])
async def get_current_model():
    """
    Get information about the current model being used in the system.
    Returns:
        Dict containing current model information including name and version.
    """
    return {
        "current_model": "Case Management Model",
        "model_version": "1.0.0",
        "status": "active",
        "last_updated": "2024-03-25"
    }
    
@app.get("/api/available-models", response_model=Dict[str, list])
async def get_available_models():
    """
    Get a list of available machine learning models supported by the system.
    Returns:
        Dict containing a list of model names.
    """
    return {
        "available_models": [
            "logistic_regression",
            "decision_tree",
            "random_forest"
        ]
    }
