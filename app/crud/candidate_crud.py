"""
This module contains functions related to candidate management, including creating,
retrieving, updating, and deleting candidates.

It interacts with the database via SQLAlchemy sessions and performs
various operations related to candidates, such as checking for the existence of
associated users, updating application statuses, and returning candidate details.

Functions:
- create_candidate: Creates a new candidate record in the database.
- get_candidate: Retrieves a candidate by their ID.
- get_all_candidates: Retrieves all candidates from the database.
- update_application_status: Updates the application status of a candidate.
- delete_candidate: Deletes a candidate by their ID.

Exceptions:
- UserNotFoundError: Raised if a user or candidate is not found during certain operations.

Modules Imported:
- Session: SQLAlchemy's session class for interacting with the database.
- Candidate, User: SQLAlchemy models representing candidates and users.
- CandidateCreate, CandidateResponse: Pydantic schemas for input validation and response formatting.
"""

from typing import List
# from typing import Union

from sqlalchemy.orm import Session # joinedload

from app.exceptions import UserNotFoundError
from app.models.model import Candidate, User
from app.schema.schema import CandidateCreate, CandidateResponse # UserCreate


# Create a new candidate
def create_candidate(
        db: Session,
        candidate: CandidateCreate
) -> CandidateResponse:
    """
    Creates a new candidate and stores it in the database.

    Args:
        db (Session): The database session to interact with the database.
        candidate (CandidateCreate): The data for the candidate to be created.

    Returns:
        CandidateResponse: The response model containing
        the candidate's details, including user information.

    Raises:
        UserNotFoundError: If the user ID associated with the
                           candidate does not exist in the database.
    """
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
def get_candidate(
        db: Session,
        candidate_id: int
) -> CandidateResponse:
    """
    Retrieves a candidate by their ID from the database.

    Args:
        db (Session): The database session to interact with the database.
        candidate_id (int): The ID of the candidate to retrieve.

    Returns:
        CandidateResponse: The response model containing the candidate's details,
        including user information.

    Raises:
        UserNotFoundError: If the candidate with the given ID does not exist in the database.
    """
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
    """
    Retrieves all candidates from the database.

    Args:
        db (Session): The database session to interact with the database.

    Returns:
        List[CandidateResponse]: A list of response models,
                        each containing a candidate's details and user information.
    """
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
def update_application_status(
        db: Session,
        candidate_id: int,
        application_status: str) -> CandidateResponse:
    """
    Updates the application status of a candidate.

    Args:
        db (Session): The database session to interact with the database.
        candidate_id (int): The ID of the candidate whose application status is to be updated.
        application_status (str): The new application status for the candidate.

    Returns:
        CandidateResponse: The updated candidate details,
                           including the new application status and user information.

    Raises:
        UserNotFoundError: If the candidate with the given ID does not exist in the database.
    """
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
    """
    Updates the application status of a candidate.

    Args:
        db (Session): The database session to interact with the database.
        candidate_id (int): The ID of the candidate whose application status is to be updated.
        application_status (str): The new application status for the candidate.

    Returns:
        CandidateResponse: The updated candidate details,
                           including the new application status and user information.

    Raises:
        UserNotFoundError: If the candidate with the given ID does not exist in the database.
    """
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if db_candidate:
        db.delete(db_candidate)
        db.commit()
        return True
    return False
