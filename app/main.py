"""
This module sets up and configures the FastAPI application,
including middleware, database initialization, and API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import router as api_router  # Import the router from api.py
from app.database.database import engine, Base  # For database initialization

# from app.clients.router import router as clients_router

app = FastAPI()

# Set API endpoints on router

# old server

# app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Initialize the database tables (this is typically done once on app startup)
Base.metadata.create_all(bind=engine)

# Register the API router
app.include_router(api_router, prefix="/api", tags=["API"])

# Define a basic root endpoint to check if the server is running
@app.get("/")
def read_root():
    """
        Root endpoint that returns a welcome message when accessed.
        This is typically used to check if the server is running.
    """
    return {"message": "Welcome to the FastAPI application!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
