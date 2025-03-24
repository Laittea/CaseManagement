"""
Client case repository implementation for data access operations.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import ClientCase, User, Client
from app.core.repository import IRepository

class ClientCaseRepository(IRepository[ClientCase]):
    """Repository for ClientCase entity operations."""

    def get_by_id(self, db: Session, id: int) -> Optional[ClientCase]:
        """Get case by composite ID (client_id, user_id)."""
        client_id, user_id = id  # Unpack tuple of IDs
        case = db.query(ClientCase).filter(
            ClientCase.client_id == client_id,
            ClientCase.user_id == user_id
        ).first()
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case not found for client {client_id} and user {user_id}"
            )
        return case

    def get_all(self, db: Session, skip: int = 0, limit: int = 50) -> List[ClientCase]:
        """Get all cases with pagination."""
        return db.query(ClientCase).offset(skip).limit(limit).all()

    def create(self, db: Session, entity: ClientCase) -> ClientCase:
        """Create a new case assignment."""
        try:
            # Verify client exists
            client = db.query(Client).filter(Client.id == entity.client_id).first()
            if not client:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Client with id {entity.client_id} not found"
                )

            # Verify case worker exists
            case_worker = db.query(User).filter(User.id == entity.user_id).first()
            if not case_worker:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Case worker with id {entity.user_id} not found"
                )

            # Check if assignment already exists
            existing_case = db.query(ClientCase).filter(
                ClientCase.client_id == entity.client_id,
                ClientCase.user_id == entity.user_id
            ).first()

            if existing_case:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Client {entity.client_id} already has a case assigned to case worker {entity.user_id}"
                )

            db.add(entity)
            db.commit()
            db.refresh(entity)
            return entity
        except HTTPException:
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case: {str(e)}"
            )

    def update(self, db: Session, id: int, data: Dict[str, Any]) -> ClientCase:
        """Update an existing case."""
        case = self.get_by_id(db, id)
        for field, value in data.items():
            setattr(case, field, value)
        try:
            db.commit()
            db.refresh(case)
            return case
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update case: {str(e)}"
            )

    def delete(self, db: Session, id: int) -> None:
        """Delete a case."""
        case = self.get_by_id(db, id)
        try:
            db.delete(case)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete case: {str(e)}"
            )

    def get_by_client_id(self, db: Session, client_id: int) -> List[ClientCase]:
        """Get all cases for a specific client."""
        return db.query(ClientCase).filter(
            ClientCase.client_id == client_id
        ).all()

    def get_by_case_worker(self, db: Session, case_worker_id: int) -> List[ClientCase]:
        """Get all cases assigned to a specific case worker."""
        return db.query(ClientCase).filter(
            ClientCase.user_id == case_worker_id
        ).all()

    def get_by_services(self, db: Session, service_filters: Dict[str, bool]) -> List[ClientCase]:
        """Get cases filtered by service statuses."""
        query = db.query(ClientCase)
        for service_name, status in service_filters.items():
            if status is not None:
                query = query.filter(getattr(ClientCase, service_name) == status)
        return query.all() 