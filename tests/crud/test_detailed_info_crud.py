import pytest
from datetime import datetime
from app.crud import detailed_info_crud
from app.models.model import User, Candidate, UserRole
from app.schema.schema import DetailedInfoCreate
from sqlalchemy.orm import Session

def create_candidate(db: Session):
    user = User(
        name="Test Candidate",
        email="test_candidate@example.com",
        password="testpassword",
        role=UserRole.CANDIDATE
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    candidate = Candidate(
        user_id=user.id,
        application_date=datetime.utcnow(),
        application_status="Pending"
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def test_create_detailed_info(db_session):
    candidate = create_candidate(db_session)
    detailed_info_data = DetailedInfoCreate(
        attending_school="Test University",
        level_of_schooling="Bachelor's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=3,
        canada_work_ex=1,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    response = detailed_info_crud.create_detailed_info(
        db=db_session,
        detailed_info=detailed_info_data,
        candidate_id=candidate.id
    )
    assert response.id is not None
    assert response.attending_school == "Test University"

def test_get_detailed_info_by_candidate(db_session):
    candidate = create_candidate(db_session)
    # First, create detailed info
    detailed_info_data = DetailedInfoCreate(
        attending_school="Test University",
        # Provide default values for required fields
        level_of_schooling="Bachelor's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=3,
        canada_work_ex=1,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    detailed_info_crud.create_detailed_info(
        db=db_session,
        detailed_info=detailed_info_data,
        candidate_id=candidate.id
    )
    # Now, retrieve it
    response = detailed_info_crud.get_detailed_info_by_candidate(
        db=db_session,
        candidate_id=candidate.id
    )
    assert response is not None
    assert response.attending_school == "Test University"

def test_update_detailed_info(db_session):
    candidate = create_candidate(db_session)
    detailed_info_data = DetailedInfoCreate(
        attending_school="Old University",
        # Provide default values for required fields
        level_of_schooling="Bachelor's",
        fluent_english_scale="Intermediate",
        reading_english_scale=4,
        speaking_english_scale=4,
        writing_english_scale=4,
        numeracy_scale=4,
        computer_scale=4,
        work_experience=2,
        canada_work_ex=0,
        currently_employed="No",
        income_source="None",
        time_unemployed=6,
        substance_use="No",
        caregiver_bool="Yes",
        housing_bool="Yes",
        need_mental_health_support_bool="Yes",
        transportation_bool="No",
        felony_bool="No"
    )
    created_info = detailed_info_crud.create_detailed_info(
        db=db_session,
        detailed_info=detailed_info_data,
        candidate_id=candidate.id
    )
    updated_info_data = DetailedInfoCreate(
        attending_school="New University",
        # Update or keep default values for other required fields
        level_of_schooling="Master's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=5,
        canada_work_ex=2,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    updated_response = detailed_info_crud.update_detailed_info(
        db=db_session,
        detailed_info_id=created_info.id,
        updated_info=updated_info_data
    )
    assert updated_response.attending_school == "New University"
    assert updated_response.level_of_schooling == "Master's"

def test_delete_detailed_info(db_session):
    candidate = create_candidate(db_session)
    detailed_info_data = DetailedInfoCreate(
        attending_school="Test University",
        # Provide default values for required fields
        level_of_schooling="Bachelor's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=3,
        canada_work_ex=1,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    created_info = detailed_info_crud.create_detailed_info(
        db=db_session,
        detailed_info=detailed_info_data,
        candidate_id=candidate.id
    )
    delete_result = detailed_info_crud.delete_detailed_info(
        db=db_session,
        detailed_info_id=created_info.id
    )
    assert delete_result is True
    # Verify deletion
    try:
        detailed_info_crud.get_detailed_info_by_id(
            db=db_session,
            detailed_info_id=created_info.id
        )
    except ValueError as e:
        print(f"Exception caught: {e}")
    else:
        print("No exception raised when expected.")
        assert False, "Expected ValueError was not raised."

def test_create_detailed_info_nonexistent_candidate(db_session):
    detailed_info_data = DetailedInfoCreate(
        attending_school="Test University",
        # Provide default values for required fields
        level_of_schooling="Bachelor's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=3,
        canada_work_ex=1,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    with pytest.raises(ValueError) as excinfo:
        detailed_info_crud.create_detailed_info(
            db=db_session,
            detailed_info=detailed_info_data,
            candidate_id=999  # Non-existent candidate ID
        )
    assert "Candidate with id 999 not found." in str(excinfo.value)

def test_update_detailed_info_nonexistent(db_session):
    updated_info_data = DetailedInfoCreate(
        attending_school="Updated University",
        # Provide default values for required fields
        level_of_schooling="Master's",
        fluent_english_scale="Advanced",
        reading_english_scale=5,
        speaking_english_scale=5,
        writing_english_scale=5,
        numeracy_scale=5,
        computer_scale=5,
        work_experience=5,
        canada_work_ex=2,
        currently_employed="Yes",
        income_source="Employment",
        time_unemployed=0,
        substance_use="No",
        caregiver_bool="No",
        housing_bool="No",
        need_mental_health_support_bool="No",
        transportation_bool="Yes",
        felony_bool="No"
    )
    with pytest.raises(ValueError) as excinfo:
        detailed_info_crud.update_detailed_info(
            db=db_session,
            detailed_info_id=999,  # Non-existent DetailedInfo ID
            updated_info=updated_info_data
        )
    assert "DetailedInfo with id 999 not found." in str(excinfo.value)

def test_delete_detailed_info_nonexistent(db_session):
    with pytest.raises(ValueError) as excinfo:
        detailed_info_crud.delete_detailed_info(
            db=db_session,
            detailed_info_id=999  # Non-existent DetailedInfo ID
        )
    assert "DetailedInfo with id 999 not found." in str(excinfo.value)
