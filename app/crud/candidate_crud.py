from typing import List, Union
from sqlalchemy.orm import Session, joinedload

from app.exceptions import UserNotFoundError
from app.models.model import Candidate, User
from app.schema.schema import CandidateCreate, CandidateResponse, UserCreate


# Create a new candidate
def create_candidate(db: Session, candidate: CandidateCreate) -> CandidateResponse:
    db_user = db.query(User).filter(User.id == candidate.user_id).first()
    if not db_user:
        raise UserNotFoundError(f"User with ID {candidate.user_id} does not exist.")

    db_candidate = Candidate(
        user_id=db_user.id,
        application_date=candidate.applicationDate,
        application_status=candidate.applicationStatus,
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    return CandidateResponse(
        id=db_candidate.id,
        name=db_user.name,
        email=db_user.email,
        applicationDate=db_candidate.application_date,
        applicationStatus=db_candidate.application_status,
        user={"name": db_user.name, "email": db_user.email},
    )

# Get candidate by ID
def get_candidate(db: Session, candidate_id: int) -> CandidateResponse:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise UserNotFoundError(f"Candidate with ID {candidate_id} does not exist.")

    db_user = db.query(User).filter(User.id == db_candidate.user_id).first()

    return CandidateResponse(
        id=db_candidate.id,
        name=db_user.name,
        email=db_user.email,
        applicationDate=db_candidate.application_date,
        applicationStatus=db_candidate.application_status,
        user={"name": db_user.name, "email": db_user.email},
    )

# Get all candidates
def get_all_candidates(db: Session) -> List[CandidateResponse]:
    db_candidates = db.query(Candidate).all()
    candidate_responses = []
    for db_candidate in db_candidates:
        db_user = db.query(User).filter(User.id == db_candidate.user_id).first()
        candidate_responses.append(
            CandidateResponse(
                id=db_candidate.id,
                name=db_user.name,
                email=db_user.email,
                applicationDate=db_candidate.application_date,
                applicationStatus=db_candidate.application_status,
                user={"name": db_user.name, "email": db_user.email},
            )
        )
    return candidate_responses


# Update candidate's application status
def update_application_status(db: Session, candidate_id: int, application_status: str) -> CandidateResponse:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise UserNotFoundError(f"Candidate with ID {candidate_id} does not exist.")

    db_candidate.application_status = application_status
    db.commit()
    db.refresh(db_candidate)

    db_user = db.query(User).filter(User.id == db_candidate.user_id).first()

    return CandidateResponse(
        id=db_candidate.id,
        name=db_user.name,
        email=db_user.email,
        applicationDate=db_candidate.application_date,
        applicationStatus=db_candidate.application_status,
        user={"name": db_user.name, "email": db_user.email},
    )

# Delete a candidate
def delete_candidate(db: Session, candidate_id: int) -> bool:
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        return True
    return False