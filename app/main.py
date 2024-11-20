from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.clients.ConnectionManager import ConnectionManager
from app.clients.router import router as clients_router


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

# Test ConnectionManager
@app.get("/test-connection")
async def test_connection():
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()
        if connection.is_connected():
            connection_manager.close_connection(connection)
            return {"message": "Connection to the database was successful!"}
        else:
            raise HTTPException(status_code=500, detail="Connection to the database failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




