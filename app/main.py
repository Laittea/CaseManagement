from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.clients.router import router as clients_router
from app.clients.database import create_clients_table  # input from database.py

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

@app.on_event("startup")
async def startup_event():
    create_clients_table()

if __name__ == "__main__":
    create_clients_table()