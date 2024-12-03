from fastapi import HTTPException
from app.clients.mapper import get_client, update_client_in_db

def check_valid_input(client_id):
    """Check if the input is valid"""
    if not client_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid client_id format.")

async def update_client(client_id: str, update_data: dict):
    """Update service logic"""
    # Validate input
    check_valid_input(client_id)

    # Check if client exists
    client = get_client(client_id)
    if not client:
        raise HTTPException(
            status_code=404,
            detail=f"Client with ID {client_id} not found"
        )

    # Update the client
    try:
        update_client_in_db(client_id, update_data)
        return {
            "success": True,
            "message": f"Client {client_id} successfully updated",
            "client_id": client_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
