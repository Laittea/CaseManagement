from typing import List
from sqlalchemy.orm import Session
from app.models.model import Candidate
from app.schema.schema import CandidateCreate, CandidateResponse

# Create a new candidate
def create_candidate(db: Session, candidate: CandidateCreate) -> CandidateResponse:
    db_candidate = Candidate(
        application_date=candidate.applicationDate,
        application_status=candidate.applicationStatus,
        user_id=candidate.user_id,  # assuming `user_id` is passed as part of candidate creation
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return CandidateResponse.model_validate(db_candidate)  # Use model_validate instead of from_orm

# Get candidate by ID
def get_candidate(db: Session, candidate_id: int) -> CandidateResponse | None:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        return CandidateResponse.model_validate(db_candidate)  # Use model_validate instead of from_orm
    return None

# Get all candidates
def get_all_candidates(db: Session) -> List[CandidateResponse]:
    db_candidates = db.query(Candidate).all()
    return [CandidateResponse.model_validate(candidate) for candidate in db_candidates]  # Use model_validate

# Update candidate's application status
def update_application_status(db: Session, candidate_id: int, application_status: str) -> CandidateResponse | None:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db_candidate.application_status = application_status
        db.commit()
        db.refresh(db_candidate)
        return CandidateResponse.model_validate(db_candidate)  # Use model_validate
    return None

# Delete a candidate
def delete_candidate(db: Session, candidate_id: int) -> bool:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        return True
    return False
