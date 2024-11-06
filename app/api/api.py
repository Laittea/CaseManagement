from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.databse import get_db
from app.schema.schema import CandidateCreate, CandidateResponse, DetailedInfoCreate, DetailedInfoResponse
from app.crud.candidate_crud import create_candidate, get_candidate, get_all_candidates, update_application_status, delete_candidate
from app.crud.detailed_info_crud import create_detailed_info, get_detailed_info_by_candidate, update_detailed_info, delete_detailed_info

router = APIRouter()

# only contains candidates and detail information
# TODO: adding user's api

# Candidate Routes

@router.post("/candidates/", response_model=CandidateResponse)
def create_candidate_route(candidate: CandidateCreate, db: Session = Depends(get_db)):
    return create_candidate(db=db, candidate=candidate)

@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
    db_candidate = get_candidate(db=db, candidate_id=candidate_id)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.get("/candidates/", response_model=List[CandidateResponse])
def get_all_candidates_route(db: Session = Depends(get_db)):
    return get_all_candidates(db=db)

@router.put("/candidates/{candidate_id}", response_model=CandidateResponse)
def update_application_status_route(candidate_id: int, application_status: str, db: Session = Depends(get_db)):
    db_candidate = update_application_status(db=db, candidate_id=candidate_id, application_status=application_status)
    if db_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return db_candidate

@router.delete("/candidates/{candidate_id}", response_model=dict)
def delete_candidate_route(candidate_id: int, db: Session = Depends(get_db)):
    success = delete_candidate(db=db, candidate_id=candidate_id)
    if not success:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}

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
