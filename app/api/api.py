"""
This module contains the FastAPI routes for managing users, candidates, and detailed information.

Routes:
- POST /users/       - Create a new user
- GET /users/{id}    - Retrieve a user by ID
- GET /users/        - Retrieve all users with pagination
- DELETE /users/{id} - Delete a user by ID
- POST /candidates/  - Create a new candidate
- GET /candidates/{id} - Retrieve a candidate by ID
- PUT /candidates/{id} - Update a candidate's application status
- DELETE /candidates/{id} - Delete a candidate by ID
- POST /detailed_info/ - Create detailed information for a candidate
- GET /detailed_info/{candidate_id} - Retrieve detailed info by candidate ID
- PUT /detailed_info/{detailed_info_id} - Update detailed info
- DELETE /detailed_info/{detailed_info_id} - Delete detailed info
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud.user_crud import create_user, get_user, get_users, delete_user
from app.database.database import get_db
from app.exceptions import UserNotFoundError
from app.schema.schema import (CandidateCreate, CandidateResponse, DetailedInfoCreate, \
                               DetailedInfoResponse, UserResponse, UserCreate)
from app.crud.candidate_crud import (create_candidate, get_candidate, get_all_candidates, \
                                     update_application_status, delete_candidate)
from app.crud.detailed_info_crud import (create_detailed_info, get_detailed_info_by_candidate, \
                                         update_detailed_info, delete_detailed_info, \
                                         get_detailed_info_by_id)

router = APIRouter()

# only contains candidates and detail information
@router.post("/users/", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
        Creates a new user in the database.

        Args:
            user (UserCreate): The user data to be created.
            db (Session): The database session.

        Returns:
            UserResponse: The created user response.

        Raises:
            HTTPException: If an error occurs while creating the user.
    """
    try:
        return create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    """
        Retrieves a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to retrieve.
            db (Session): The database session.

        Returns:
            UserResponse: The user response.

        Raises:
            HTTPException: If the user is not found or if an unexpected error occurs.
    """
    try:
        db_user = get_user(db=db, user_id=user_id)
        if not db_user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        return db_user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e

@router.get("/users/", response_model=List[UserResponse])
def get_users_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
        Retrieves a list of users with pagination.

        Args:
            skip (int): The number of users to skip for pagination (default 0).
            limit (int): The maximum number of users to return (default 10).
            db (Session): The database session.

        Returns:
            List[UserResponse]: A list of user responses.
    """
    return get_users(db=db, skip=skip, limit=limit)

@router.delete("/users/{user_id}", response_model=dict)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    """
        Deletes a user by their ID from the database.

        Args:
            user_id (int): The ID of the user to delete.
            db (Session): The database session.

        Returns:
            dict: A message indicating success.

        Raises:
            HTTPException: If the user is not found.
    """
    user = delete_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
# Candidate Routes

@router.post("/candidates/", response_model=CandidateResponse)
async def create_candidate_route(candidate: CandidateCreate, db: Session = Depends(get_db)):
    """
        Creates a new candidate in the database.

        Args:
            candidate (CandidateCreate): The candidate data to be created.
            db (Session): The database session.

        Returns:
            CandidateResponse: The created candidate response.

        Raises:
            HTTPException: If the candidate creation fails.
    """
    try:
        return create_candidate(db=db, candidate=candidate)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while creating the candidate: {str(e)}"
        ) from e

@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
    """
        Retrieves a candidate by their ID from the database.

        Args:
            candidate_id (int): The ID of the candidate to retrieve.
            db (Session): The database session.

        Returns:
            CandidateResponse: The retrieved candidate response.

        Raises:
            HTTPException: If the candidate is not found or if an unexpected error occurs.
    """
    try:
        db_candidate = get_candidate(db=db, candidate_id=candidate_id)
        if not db_candidate:
            raise UserNotFoundError(f"Candidate with ID {candidate_id} does not exist.")
        return db_candidate
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e

@router.get("/candidates/", response_model=List[CandidateResponse])
def get_all_candidates_route(db: Session = Depends(get_db)):
    """
        Retrieves all candidates from the database.

        Args:
            db (Session): The database session.

        Returns:
            List[CandidateResponse]: A list of candidate responses.
    """
    return get_all_candidates(db=db)

@router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
def update_application_status_route(
        candidate_id: int,
        application_status: str,
        db: Session = Depends(get_db)
):
    """
        Updates the application status of a candidate.

        Args:
            candidate_id (int): The ID of the candidate to update.
            application_status (str): The new application status to set.
            db (Session): The database session.

        Returns:
            CandidateResponse: The updated candidate response.

        Raises:
            HTTPException: If the candidate is not found or if an unexpected error occurs.
    """
    try:
        db_candidate = update_application_status(
            db=db,
            candidate_id=candidate_id,
            application_status=application_status
        )
        return db_candidate
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


@router.delete("/candidates/{candidate_id}", response_model=dict)
def delete_candidate_route(
        candidate_id: int,
        db: Session = Depends(get_db)
):
    """
    Deletes a candidate by their ID from the database.

    Args:
        candidate_id (int): The ID of the candidate to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating success.

    Raises:
        HTTPException: If the candidate is not found or if deletion fails.
    """
    try:
        db_candidate = get_candidate(db=db, candidate_id=candidate_id)
        if not db_candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} does not exist."
            )
        success = delete_candidate(db=db, candidate_id=candidate_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to delete Candidate with ID {candidate_id}."
            )
        return {"message": "Candidate deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting the candidate: {str(e)}"
        ) from e

# DetailedInfo Routes

@router.post("/detailed_info/", response_model=DetailedInfoResponse)
def create_detailed_info_route(
        detailed_info: DetailedInfoCreate,
        candidate_id: int,
        db: Session = Depends(get_db)
):
    """
    Creates detailed information for a candidate.

    Args:
        detailed_info (DetailedInfoCreate): The detailed information to create.
        candidate_id (int): The ID of the candidate for whom the information is being created.
        db (Session): The database session.

    Returns:
        DetailedInfoResponse: The created detailed information response.

    Raises:
        HTTPException: If the candidate is not found or if an error
                       occurs while creating the information.
    """
    try:
        db_candidate = get_candidate(db=db, candidate_id=candidate_id)
        if not db_candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} does not exist.",
            )
        return create_detailed_info(db=db, detailed_info=detailed_info, candidate_id=candidate_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating detailed info: {str(e)}",
        ) from e
@router.get("/detailed_info/{candidate_id}", response_model=DetailedInfoResponse)
def get_detailed_info_by_candidate_route(
        candidate_id: int,
        db: Session = Depends(get_db)
):
    """
    Retrieves detailed information for a specific candidate.

    Args:
        candidate_id (int): The ID of the candidate for whom to retrieve detailed information.
        db (Session): The database session.

    Returns:
        DetailedInfoResponse: The detailed information for the specified candidate.

    Raises:
        HTTPException: If the candidate or the detailed information is not found.
    """
    try:
        db_candidate = get_candidate(db=db, candidate_id=candidate_id)
        if not db_candidate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Candidate with ID {candidate_id} does not exist.",
            )
        db_detailed_info = get_detailed_info_by_candidate(db=db, candidate_id=candidate_id)
        if not db_detailed_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detailed info not found for candidate ID {candidate_id}.",
            )
        return db_detailed_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        ) from e

@router.put("/detailed_info/{detailed_info_id}", response_model=DetailedInfoResponse)
def update_detailed_info_route(
        detailed_info_id: int,
        updated_info: DetailedInfoCreate,
        db: Session = Depends(get_db)
):
    """
    Updates detailed information for a candidate.

    Args:
        detailed_info_id (int): The ID of the detailed information to update.
        updated_info (DetailedInfoCreate): The updated detailed information.
        db (Session): The database session.

    Returns:
        DetailedInfoResponse: The updated detailed information response.

    Raises:
        HTTPException: If the detailed information is not found or if an unexpected error occurs.
    """
    try:
        db_detailed_info = get_detailed_info_by_id(db=db, detailed_info_id=detailed_info_id)
        if not db_detailed_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detailed info with ID {detailed_info_id} does not exist.",
            )
        return update_detailed_info(
            db=db,
            detailed_info_id=detailed_info_id,
            updated_info=updated_info
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        ) from e

@router.delete("/detailed_info/{detailed_info_id}", response_model=dict)
def delete_detailed_info_route(
        detailed_info_id: int,
        db: Session = Depends(get_db)
):
    """
    Deletes detailed information for a candidate.

    Args:
        detailed_info_id (int): The ID of the detailed information to delete.
        db (Session): The database session.

    Returns:
        dict: A message indicating success.

    Raises:
        HTTPException: If the detailed information is not found or if deletion fails.
    """
    try:
        db_detailed_info = get_detailed_info_by_id(db=db, detailed_info_id=detailed_info_id)
        if not db_detailed_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detailed info with ID {detailed_info_id} does not exist.",
            )
        success = delete_detailed_info(db=db, detailed_info_id=detailed_info_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to delete detailed info with ID {detailed_info_id}.",
            )
        return {"message": "Detailed info deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while deleting detailed info: {str(e)}",
        ) from e
