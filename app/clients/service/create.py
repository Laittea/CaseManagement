from fastapi import HTTPException

from app.clients.mapper import create_client_in_db
from app.clients.service.update_model import ClientUpdateModel


async def create_client(client_data: ClientUpdateModel):
    validated_data = client_data

    try:
        client_id = create_client_in_db(validated_data)
        return {
            "success": True,
            "message": f"Client successfully created with ID {client_id}",
            "client_id": client_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
