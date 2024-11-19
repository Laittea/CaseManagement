from fastapi import HTTPException


async def retrieve_client(client_id: str):
    try:
        # Check if client exists
        if client_id not in database:
            raise Exception("Client not found")

        # Return client information
        return {
            "success": True,
            "data": database[client_id]
        }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Client with ID {client_id} not found"
        )
