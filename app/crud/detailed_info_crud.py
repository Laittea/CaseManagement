"""
CRUD operations for DetailedInfo model.

This module contains the following CRUD functions for managing detailed information
associated with candidates:

- create_detailed_info: Create a new detailed information record for a candidate.
- update_detailed_info: Update the detailed information record for a specific candidate.
- get_detailed_info_by_candidate: Retrieve the detailed information
                                  for a specific candidate by candidate ID.
- get_detailed_info_by_id: Retrieve the detailed information by its unique ID.
- delete_detailed_info: Delete a specific detailed information record.

Each function interacts with the database session
and validates the data related to candidates and their detailed information.
"""

from sqlalchemy.orm import Session
from app.models.model import DetailedInfo, Candidate
from app.schema.schema import DetailedInfoCreate, DetailedInfoResponse

# app/crud/detailed_info_crud.py

def create_detailed_info(db: Session, detailed_info: DetailedInfoCreate, candidate_id: int):
    """
    Create a new detailed information record for a candidate.

    Args:
        db (Session): The database session.
        detailed_info (DetailedInfoCreate): The detailed information to be created.
        candidate_id (int): The ID of the candidate for
                            whom the detailed information is being created.

    Raises:
        ValueError: If the candidate with the given candidate_id is not found.

    Returns:
        DetailedInfoResponse: The created detailed information record.
    """
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        raise ValueError(f"Candidate with id {candidate_id} not found.")

    db_detailed_info = DetailedInfo(
        candidate_id=candidate_id,
        **detailed_info.model_dump()
    )
    db.add(db_detailed_info)
    db.commit()
    db.refresh(db_detailed_info)
    return DetailedInfoResponse.model_validate(db_detailed_info)

def update_detailed_info(db: Session, detailed_info_id: int, updated_info: DetailedInfoCreate):
    """
    Update the detailed information record for a specific candidate.

    Args:
        db (Session): The database session.
        detailed_info_id (int): The ID of the detailed information record to be updated.
        updated_info (DetailedInfoCreate): The updated detailed information.

    Raises:
        ValueError: If the detailed information with the given detailed_info_id is not found.

    Returns:
        DetailedInfoResponse: The updated detailed information record.
    """
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")

    for key, value in updated_info.model_dump().items():
        setattr(db_detailed_info, key, value)
    db.commit()
    db.refresh(db_detailed_info)
    return DetailedInfoResponse.model_validate(db_detailed_info)

def get_detailed_info_by_candidate(db: Session, candidate_id: int):
    """
    Retrieve the detailed information for a specific candidate by candidate ID.

    Args:
        db (Session): The database session.
        candidate_id (int): The ID of the candidate whose detailed information is being retrieved.

    Returns:
        DetailedInfoResponse | None: The detailed information
                                     for the candidate if found, otherwise None.
    """
    db_detailed_info = (
        db.query(DetailedInfo)
        .filter(DetailedInfo.candidate_id == candidate_id)
        .first())
    return DetailedInfoResponse.model_validate(db_detailed_info) if db_detailed_info else None


def get_detailed_info_by_id(db: Session, detailed_info_id: int):
    """
    Retrieve the detailed information by its unique ID.

    Args:
        db (Session): The database session.
        detailed_info_id (int): The ID of the detailed information to be retrieved.

    Raises:
        ValueError: If the detailed information with the given detailed_info_id is not found.

    Returns:
        DetailedInfoResponse: The detailed information record with the given ID.
    """
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        print(f"DetailedInfo with id {detailed_info_id} not found.")  # Debug statement
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")
    print(f"Retrieved DetailedInfo with id {detailed_info_id}")  # Debug statement
    return DetailedInfoResponse.model_validate(db_detailed_info)

def delete_detailed_info(db: Session, detailed_info_id: int):
    """
    Delete a specific detailed information record.

    Args:
        db (Session): The database session.
        detailed_info_id (int): The ID of the detailed information to be deleted.

    Raises:
        ValueError: If the detailed information with the given detailed_info_id is not found.

    Returns:
        bool: True if the detailed information was deleted successfully.
    """
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")
    db.delete(db_detailed_info)
    db.commit()
    return True
