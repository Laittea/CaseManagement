"""
Base repository interfaces for data access layer.
"""

from typing import Generic, TypeVar, Optional, List, Any
from sqlalchemy.orm import Session

T = TypeVar("T")


class IRepository(Generic[T]):
    """Base repository interface defining common data access operations."""

    def get_by_id(self, db: Session, id: int) -> Optional[T]:
        """Get entity by ID."""
        raise NotImplementedError

    def get_all(self, db: Session, skip: int = 0, limit: int = 50) -> List[T]:
        """Get all entities with pagination."""
        raise NotImplementedError

    def create(self, db: Session, entity: T) -> T:
        """Create a new entity."""
        raise NotImplementedError

    def update(self, db: Session, id: int, data: dict[str, Any]) -> T:
        """Update an existing entity."""
        raise NotImplementedError

    def delete(self, db: Session, id: int) -> None:
        """Delete an entity."""
        raise NotImplementedError
