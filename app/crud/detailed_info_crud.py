from sqlalchemy.orm import Session
from app.models.model import DetailedInfo, Candidate
from app.schema.schema import DetailedInfoCreate, DetailedInfoResponse

# Create detailed information for a candidate
def create_detailed_info(db: Session, detailed_info: DetailedInfoCreate, candidate_id: int) -> DetailedInfoResponse | None:
    # Check if the candidate exists
    db_candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not db_candidate:
        return None  # Candidate does not exist

    # Create a new DetailedInfo instance
    db_detailed_info = DetailedInfo(
        candidate_id=candidate_id,
        attending_school=detailed_info.attendingSchool,
        level_of_schooling=detailed_info.levelOfSchooling,
        fluent_english=detailed_info.fluentEnglishScale,
        reading_english_scale=detailed_info.readingEnglishScale,
        speaking_english_scale=detailed_info.speakingEnglishScale,
        writing_english_scale=detailed_info.writingEnglishScale,
        numeracy_scale=detailed_info.numeracyScale,
        computer_scale=detailed_info.computerScale,
        work_experience=detailed_info.workExperience,
        canada_work_ex=detailed_info.canadaWorkEx,
        currently_employed=detailed_info.currentlyEmployed,
        income_source=detailed_info.incomeSource,
        time_unemployed=detailed_info.timeUnemployed,
        substance_use=detailed_info.substance_use,
        caregiver_bool=detailed_info.caregiverBool,
        housing_bool=detailed_info.housingBool,
        need_mental_health_support_bool=detailed_info.needMentalHealthSupportBool,
        transportation_bool=detailed_info.transportationBool,
        felony_bool=detailed_info.felonyBool
    )

    db.add(db_detailed_info)
    db.commit()
    db.refresh(db_detailed_info)
    return DetailedInfoResponse.model_validate(db_detailed_info)  # Use model_validate to return a response

# Get detailed info for a candidate by candidate ID
def get_detailed_info_by_candidate(db: Session, candidate_id: int) -> DetailedInfoResponse | None:
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.candidate_id == candidate_id).first()
    if db_detailed_info:
        return DetailedInfoResponse.model_validate(db_detailed_info)  # Use model_validate
    return None

# Get detailed info by detailed info ID
def get_detailed_info_by_id(db: Session, detailed_info_id: int) -> DetailedInfoResponse | None:
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if db_detailed_info:
        return DetailedInfoResponse.model_validate(db_detailed_info)  # Use model_validate
    return None

# Update detailed information for a candidate
def update_detailed_info(db: Session, detailed_info_id: int, updated_info: DetailedInfoCreate) -> DetailedInfoResponse | None:
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if db_detailed_info:
        db_detailed_info.attending_school = updated_info.attendingSchool
        db_detailed_info.level_of_schooling = updated_info.levelOfSchooling
        db_detailed_info.fluent_english = updated_info.fluentEnglishScale
        db_detailed_info.reading_english_scale = updated_info.readingEnglishScale
        db_detailed_info.speaking_english_scale = updated_info.speakingEnglishScale
        db_detailed_info.writing_english_scale = updated_info.writingEnglishScale
        db_detailed_info.numeracy_scale = updated_info.numeracyScale
        db_detailed_info.computer_scale = updated_info.computerScale
        db_detailed_info.work_experience = updated_info.workExperience
        db_detailed_info.canada_work_ex = updated_info.canadaWorkEx
        db_detailed_info.currently_employed = updated_info.currentlyEmployed
        db_detailed_info.income_source = updated_info.incomeSource
        db_detailed_info.time_unemployed = updated_info.timeUnemployed
        db_detailed_info.substance_use = updated_info.substance_use
        db_detailed_info.caregiver_bool = updated_info.caregiverBool
        db_detailed_info.housing_bool = updated_info.housingBool
        db_detailed_info.need_mental_health_support_bool = updated_info.needMentalHealthSupportBool
        db_detailed_info.transportation_bool = updated_info.transportationBool
        db_detailed_info.felony_bool = updated_info.felonyBool

        db.commit()
        db.refresh(db_detailed_info)
        return DetailedInfoResponse.model_validate(db_detailed_info)  # Use model_validate
    return None

# Delete detailed information for a candidate
def delete_detailed_info(db: Session, detailed_info_id: int) -> bool:
    db_detailed_info = db.query(DetailedInfo).filter(DetailedInfo.id == detailed_info_id).first()
    if db_detailed_info:
        db.delete(db_detailed_info)
        db.commit()
        return True
    return False
