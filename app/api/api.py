from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.crud.user_crud import create_user, get_user, get_users, delete_user
from app.database.database import get_db
from app.exceptions import UserNotFoundError
from app.schema.schema import CandidateCreate, CandidateResponse, DetailedInfoCreate, DetailedInfoResponse, \
    UserResponse, UserCreate
from app.crud.candidate_crud import create_candidate, get_candidate, get_all_candidates, update_application_status, delete_candidate
from app.crud.detailed_info_crud import create_detailed_info, get_detailed_info_by_candidate, update_detailed_info, delete_detailed_info

router = APIRouter()

# only contains candidates and detail information
# TODO: adding user's api
@router.post("/users/", response_model=UserResponse)
async def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_route(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db=db, user_id=user_id)
        if not db_user:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")
        return db_user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/users/", response_model=List[UserResponse])
def get_users_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)

@router.delete("/users/{user_id}", response_model=dict)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
# Candidate Routes

@router.post("/candidates/", response_model=CandidateResponse)
async def create_candidate_route(candidate: CandidateCreate, db: Session = Depends(get_db)):
    try:
        return create_candidate(db=db, candidate=candidate)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An error occurred while creating the candidate: {str(e)}"
        )

@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
    try:
        db_candidate = get_candidate(db=db, candidate_id=candidate_id)
        if not db_candidate:
            raise UserNotFoundError(f"Candidate with ID {candidate_id} does not exist.")
        return db_candidate
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/candidates/", response_model=List[CandidateResponse])
def get_all_candidates_route(db: Session = Depends(get_db)):
    return get_all_candidates(db=db)

@router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
def update_application_status_route(candidate_id: int, application_status: str, db: Session = Depends(get_db)):
    try:
        db_candidate = update_application_status(db=db, candidate_id=candidate_id, application_status=application_status)
        return db_candidate
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.delete("/candidates/{candidate_id}", response_model=dict)
def delete_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
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
        )

# DetailedInfo Routes

@router.post("/detailed_info/", response_model=DetailedInfoResponse)
def create_detailed_info_route(detailed_info: DetailedInfoCreate, candidate_id: int, db: Session = Depends(get_db)):
    return create_detailed_info(db=db, detailed_info=detailed_info, candidate_id=candidate_id)

@router.get("/detailed_info/{candidate_id}", response_model=DetailedInfoResponse)
def get_detailed_info_by_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
    db_detailed_info = get_detailed_info_by_candidate(db=db, candidate_id=candidate_id)
    if db_detailed_info is None:
        raise HTTPException(status_code=404, detail="Detailed info not found for this candidate")
    return db_detailed_info

@router.put("/detailed_info/{detailed_info_id}", response_model=DetailedInfoResponse)
def update_detailed_info_route(detailed_info_id: int, updated_info: DetailedInfoCreate, db: Session = Depends(get_db)):
    db_detailed_info = update_detailed_info(db=db, detailed_info_id=detailed_info_id, updated_info=updated_info)
    if db_detailed_info is None:
        raise HTTPException(status_code=404, detail="Detailed info not found")
    return db_detailed_info

@router.delete("/detailed_info/{detailed_info_id}", response_model=dict)
def delete_detailed_info_route(detailed_info_id: int, db: Session = Depends(get_db)):
    success = delete_detailed_info(db=db, detailed_info_id=detailed_info_id)
    if not success:
        raise HTTPException(status_code=404, detail="Detailed info not found")
    return {"message": "Detailed info deleted successfully"}
