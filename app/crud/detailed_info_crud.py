from sqlalchemy.orm import Session
from app.models.model import DetailedInfo, Candidate
from app.schema.schema import DetailedInfoCreate, DetailedInfoResponse

# app/crud/detailed_info_crud.py

def create_detailed_info(db: Session, detailed_info: DetailedInfoCreate, candidate_id: int):
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
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")

    for key, value in updated_info.model_dump().items():
        setattr(db_detailed_info, key, value)
    db.commit()
    db.refresh(db_detailed_info)
    return DetailedInfoResponse.model_validate(db_detailed_info)

def get_detailed_info_by_candidate(db: Session, candidate_id: int):
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.candidate_id == candidate_id).first()
    return DetailedInfoResponse.model_validate(db_detailed_info) if db_detailed_info else None


def get_detailed_info_by_id(db: Session, detailed_info_id: int):
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        print(f"DetailedInfo with id {detailed_info_id} not found.")  # Debug statement
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")
    print(f"Retrieved DetailedInfo with id {detailed_info_id}")  # Debug statement
    return DetailedInfoResponse.model_validate(db_detailed_info)

def delete_detailed_info(db: Session, detailed_info_id: int):
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if not db_detailed_info:
        raise ValueError(f"DetailedInfo with id {detailed_info_id} not found.")
    db.delete(db_detailed_info)
    db.commit()
    return True
