from pydantic import BaseModel, Field, field_serializer


class PredictionInput(BaseModel):
    # TODO: keep the field order the same as in model.py by reading a config file
    """
    PredictionInput is the validated input from webpage users

    FILED ORDER is preserved in the model schema, which will represent the same order when calling the prediction model

    validation_alias is used for validating the json format data sending from front end
    serialization_alias is used as column name when dumping the data model

    Fields in str format are converted into numerical types in  @field_serializer decorator
    """
    age: int = Field(..., validation_alias='age', serialization_alias='age')
    gender: str = Field(..., validation_alias='gender', serialization_alias='gender')
    work_experience: int = Field(..., validation_alias='work_experience', serialization_alias='work_experience')
    canada_workex: int = Field(..., validation_alias='canada_workex', serialization_alias='canada_workex')
    dep_num: int = Field(..., validation_alias='dep_num', serialization_alias='dep_num')
    canada_born: str = Field(..., validation_alias='canada_born', serialization_alias='canada_born')
    citizen_status: str = Field(..., validation_alias='citizen_status', serialization_alias='citizen_status')
    level_of_schooling: str = Field(..., validation_alias='level_of_schooling', serialization_alias='level_of_schooling')
    fluent_english: str = Field(..., validation_alias='fluent_english', serialization_alias='fluent_english')
    reading_english_scale: int = Field(..., validation_alias='reading_english_scale', serialization_alias='reading_english_scale')
    speaking_english_scale: int = Field(..., validation_alias='speaking_english_scale', serialization_alias='speaking_english_scale')
    writing_english_scale: int = Field(..., validation_alias='writing_english_scale', serialization_alias='writing_english_scale')
    numeracy_scale: int = Field(..., validation_alias='numeracy_scale', serialization_alias='numeracy_scale')
    computer_scale: int = Field(..., validation_alias='computer_scale', serialization_alias='computer_scale')
    transportation_bool: str = Field(..., validation_alias='transportation_bool', serialization_alias='transportation_bool')
    caregiver_bool: str = Field(..., validation_alias='caregiver_bool', serialization_alias='caregiver_bool')
    housing: str = Field(..., validation_alias='housing', serialization_alias='housing')
    income_source: str = Field(..., validation_alias='income_source', serialization_alias='income_source')
    felony_bool: str = Field(..., validation_alias='felony_bool', serialization_alias='felony_bool')
    attending_school: str = Field(..., validation_alias='attending_school', serialization_alias='attending_school')
    currently_employed: str = Field(..., validation_alias='currently_employed', serialization_alias='currently_employed')
    substance_use: str = Field(..., validation_alias='substance_use', serialization_alias='substance_use')
    time_unemployed: int = Field(..., validation_alias='time_unemployed', serialization_alias='time_unemployed')
    need_mental_health_support_bool: str = Field(..., validation_alias='need_mental_health_support_bool', serialization_alias='need_mental_health_support_bool')

    @field_serializer('gender')
    def serialize_age(self, gender: str):
        return 1 if gender == 'M' else 2

    @field_serializer('canada_born')
    def serialize_canada_born(self, canada_born: str):
        return 1 if canada_born == 'true' else 0

    @field_serializer('citizen_status')
    def serialize_citizen_status(self, citizen_status: str):
        match citizen_status:
            case 'citizen': return 0
            case 'permanent_resident': return 1
            case 'temporary_resident': return 2
