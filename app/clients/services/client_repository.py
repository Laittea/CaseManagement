from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.client import Client
from app.clients.schemas.client import ClientUpdate


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_client(self, client_id: int):
        """Fetch a client by ID"""
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found",
            )
        return client

    def get_clients(self, skip: int = 0, limit: int = 50):
        """Fetch all clients with pagination"""
        if skip < 0 or limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid pagination values",
            )

        clients = self.db.query(Client).offset(skip).limit(limit).all()
        total = self.db.query(Client).count()
        return {"clients": clients, "total": total}

    def update_client(self, client_id: int, client_update: ClientUpdate):
        """Update an existing client"""
        client = self.get_client(client_id)
        update_data = client_update.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(client, field, value)

        try:
            self.db.commit()
            self.db.refresh(client)
            return client
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}",
            )

    def delete_client(self, client_id: int):
        """Delete a client"""
        client = self.get_client(client_id)
        try:
            self.db.delete(client)
            self.db.commit()
            return {"message": f"Client {client_id} deleted successfully"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}",
            )
