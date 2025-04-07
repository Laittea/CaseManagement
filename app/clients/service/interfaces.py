"""
Service interfaces for client management following Interface Segregation Principle.
"""

from typing import Any, Dict, List, Protocol

from sqlalchemy.orm import Session

from app.clients.schema import ClientUpdate, ServiceUpdate
from app.models import Client, ClientCase


class IClientQueryService(Protocol):
    """Interface for client query operations."""

    def get_client(self, db: Session, client_id: int) -> Client:
        """Get a specific client by ID."""
        ...

    def get_clients(self, db: Session, skip: int, limit: int) -> Dict[str, Any]:
        """Get paginated list of clients."""
        ...

    def get_clients_by_criteria(self, db: Session, **criteria) -> List[Client]:
        """Get clients filtered by criteria."""
        ...

    def get_clients_by_success_rate(self, db: Session, min_rate: int) -> List[Client]:
        """Get clients with success rate above threshold."""
        ...


class IClientCommandService(Protocol):
    """Interface for client command operations."""

    def update_client(
        self, db: Session, client_id: int, client_data: ClientUpdate
    ) -> Client:
        """Update a client's information."""
        ...

    def delete_client(self, db: Session, client_id: int) -> None:
        """Delete a client."""
        ...


class ICaseQueryService(Protocol):
    """Interface for case query operations."""

    def get_client_services(self, db: Session, client_id: int) -> List[ClientCase]:
        """Get all services for a client."""
        ...

    def get_clients_by_services(self, db: Session, **service_filters) -> List[Client]:
        """Get clients filtered by services."""
        ...

    def get_clients_by_case_worker(
        self, db: Session, case_worker_id: int
    ) -> List[Client]:
        """Get clients assigned to a case worker."""
        ...


class ICaseCommandService(Protocol):
    """Interface for case command operations."""

    def update_client_services(
        self, db: Session, client_id: int, user_id: int, service_update: ServiceUpdate
    ) -> ClientCase:
        """Update client services."""
        ...

    def create_case_assignment(
        self, db: Session, client_id: int, case_worker_id: int
    ) -> ClientCase:
        """Create a new case assignment."""
        ...
