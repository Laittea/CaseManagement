from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.clients.router import router as clients_router
from app.clients.schema import PredictionInput
from app.clients.crud import create_user_in_db, get_all_user_data, get_user_by_id, update_user, delete_user
from app.clients.db_setup import create_tables

app = FastAPI()

# Set API endpoints on router
app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)
