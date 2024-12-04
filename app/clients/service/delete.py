from fastapi import HTTPException
from app.clients.mapper import get_client, delete_client_from_db

def check_valid_input(client_id):
    """Check if the input is valid"""
    if not client_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid client_id format.")

async def delete_client(client_id: str):
    """Deletion service logic"""
    # Validate input
    check_valid_input(client_id)

    # Retrieve the client
    try:
        client = get_client(client_id)
        if not client:
            raise HTTPException(
                status_code=404,
                detail=f"Client with ID {client_id} not found"
            )

        # Delete the client
        delete_client_from_db(client_id)

        return {
            "success": True,
            "message": f"Client {client_id} successfully deleted",
            "client_id": client_id
        }
    except Exception as e:
        raise e
