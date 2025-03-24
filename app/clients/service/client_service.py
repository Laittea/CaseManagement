"""
Client service implementations following SOLID principles.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Client, ClientCase
from app.clients.schema import ClientUpdate, ServiceUpdate
from app.clients.repository.client_repository import ClientRepository
from app.clients.repository.case_repository import ClientCaseRepository
from app.clients.service.interfaces import (
    IClientQueryService,
    IClientCommandService,
    ICaseQueryService,
    ICaseCommandService,
)

class ClientQueryService(IClientQueryService):
    """Implementation of client query operations."""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def get_client(self, db: Session, client_id: int) -> Client:
        return self.client_repository.get_by_id(db, client_id)
    
    def get_clients(self, db: Session, skip: int, limit: int) -> Dict[str, Any]:
        clients = self.client_repository.get_all(db, skip, limit)
        total = db.query(Client).count()
        return {"clients": clients, "total": total}
    
    def get_clients_by_criteria(self, db: Session, **criteria) -> List[Client]:
        # Map API parameters to model fields
        field_mapping = {
            'age_min': 'age',
            'employment_status': 'currently_employed',
            'education_level': 'level_of_schooling'
        }
        
        # Transform criteria to match model fields
        model_criteria = {}
        for key, value in criteria.items():
            if value is not None:
                model_key = field_mapping.get(key, key)
                if key == 'age_min':
                    model_criteria[f"{model_key}__ge"] = value
                else:
                    model_criteria[model_key] = value
        
        return self.client_repository.get_by_criteria(db, model_criteria)
    
    def get_clients_by_success_rate(self, db: Session, min_rate: int) -> List[Client]:
        return self.client_repository.get_by_success_rate(db, min_rate)

class ClientCommandService(IClientCommandService):
    """Implementation of client command operations."""
    
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository
    
    def update_client(self, db: Session, client_id: int, client_data: ClientUpdate) -> Client:
        update_data = client_data.dict(exclude_unset=True)
        return self.client_repository.update(db, client_id, update_data)
    
    def delete_client(self, db: Session, client_id: int) -> None:
        self.client_repository.delete(db, client_id)

class CaseQueryService(ICaseQueryService):
    """Implementation of case query operations."""
    
    def __init__(self, case_repository: ClientCaseRepository):
        self.case_repository = case_repository
    
    def get_client_services(self, db: Session, client_id: int) -> List[ClientCase]:
        return self.case_repository.get_by_client_id(db, client_id)
    
    def get_clients_by_services(self, db: Session, **service_filters) -> List[Client]:
        cases = self.case_repository.get_by_services(db, service_filters)
        return [case.client for case in cases]
    
    def get_clients_by_case_worker(self, db: Session, case_worker_id: int) -> List[Client]:
        cases = self.case_repository.get_by_case_worker(db, case_worker_id)
        return [case.client for case in cases]

class CaseCommandService(ICaseCommandService):
    """Implementation of case command operations."""
    
    def __init__(self, case_repository: ClientCaseRepository):
        self.case_repository = case_repository
    
    def update_client_services(
        self, db: Session, client_id: int, user_id: int, service_update: ServiceUpdate
    ) -> ClientCase:
        update_data = service_update.dict(exclude_unset=True)
        return self.case_repository.update(db, (client_id, user_id), update_data)
    
    def create_case_assignment(
        self, db: Session, client_id: int, case_worker_id: int
    ) -> ClientCase:
        new_case = ClientCase(
            client_id=client_id,
            user_id=case_worker_id,
            employment_assistance=False,
            life_stabilization=False,
            retention_services=False,
            specialized_services=False,
            employment_related_financial_supports=False,
            employer_financial_supports=False,
            enhanced_referrals=False,
            success_rate=0
        )
        return self.case_repository.create(db, new_case)
