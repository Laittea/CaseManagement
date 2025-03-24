"""
Client repository implementation for data access operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from app.models import Client, ClientCase
from app.core.repository import IRepository

class ClientRepository(IRepository[Client]):
    """Repository for Client entity operations."""

    def get_by_id(self, db: Session, id: int) -> Optional[Client]:
        """Get client by ID."""
        client = db.query(Client).filter(Client.id == id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {id} not found"
            )
        return client

    def get_all(self, db: Session, skip: int = 0, limit: int = 50) -> List[Client]:
        """Get all clients with pagination."""
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative"
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0"
            )
        return db.query(Client).offset(skip).limit(limit).all()

    def create(self, db: Session, entity: Client) -> Client:
        """Create a new client."""
        try:
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create client: {str(e)}"
            )

    def update(self, db: Session, id: int, data: Dict[str, Any]) -> Client:
        """Update an existing client."""
        client = self.get_by_id(db, id)
        for field, value in data.items():
            setattr(client, field, value)
        try:
            db.commit()
            db.refresh(client)
            return client
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )

    def delete(self, db: Session, id: int) -> None:
        """Delete a client."""
        client = self.get_by_id(db, id)
        try:
            # Delete associated client_cases first
            db.query(ClientCase).filter(ClientCase.client_id == id).delete()
            # Then delete the client
            db.delete(client)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}"
            )

    def get_by_criteria(self, db: Session, criteria: Dict[str, Any]) -> List[Client]:
        """Get clients by multiple criteria."""
        query = db.query(Client)
        filters = []
        
        for field, value in criteria.items():
            if value is not None:
                if '__' in field:
                    field_name, operator = field.split('__')
                    model_field = getattr(Client, field_name)
                    if operator == 'ge':
                        filters.append(model_field >= value)
                    elif operator == 'le':
                        filters.append(model_field <= value)
                    elif operator == 'gt':
                        filters.append(model_field > value)
                    elif operator == 'lt':
                        filters.append(model_field < value)
                else:
                    filters.append(getattr(Client, field) == value)
        
        if filters:
            query = query.filter(and_(*filters))
        
        return query.all()

    def get_by_success_rate(self, db: Session, min_rate: int) -> List[Client]:
        """Get clients with success rate above threshold."""
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100"
            )
        return db.query(Client).join(Client.cases).filter(
            ClientCase.success_rate >= min_rate
        ).all() 