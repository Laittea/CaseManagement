from pydantic import BaseModel, Field, field_serializer, model_serializer

class PredictionInput(BaseModel):
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
    canada_born: bool = Field(..., validation_alias='canada_born', serialization_alias='canada_born')
    citizen_status: str = Field(..., validation_alias='citizen_status', serialization_alias='citizen_status')
    level_of_schooling: str = Field(..., validation_alias='level_of_schooling', serialization_alias='level_of_schooling')
    fluent_english: bool = Field(..., validation_alias='fluent_english', serialization_alias='fluent_english')
    reading_english_scale: int = Field(..., validation_alias='reading_english_scale', serialization_alias='reading_english_scale')
    speaking_english_scale: int = Field(..., validation_alias='speaking_english_scale', serialization_alias='speaking_english_scale')
    writing_english_scale: int = Field(..., validation_alias='writing_english_scale', serialization_alias='writing_english_scale')
    numeracy_scale: int = Field(..., validation_alias='numeracy_scale', serialization_alias='numeracy_scale')
    computer_scale: int = Field(..., validation_alias='computer_scale', serialization_alias='computer_scale')
    transportation_bool: bool = Field(..., validation_alias='transportation_bool', serialization_alias='transportation_bool')
    caregiver_bool: bool = Field(..., validation_alias='caregiver_bool', serialization_alias='caregiver_bool')
    housing: str = Field(..., validation_alias='housing', serialization_alias='housing')
    income_source: str = Field(..., validation_alias='income_source', serialization_alias='income_source')
    felony_bool: bool = Field(..., validation_alias='felony_bool', serialization_alias='felony_bool')
    attending_school: bool = Field(..., validation_alias='attending_school', serialization_alias='attending_school')
    currently_employed: bool = Field(..., validation_alias='currently_employed', serialization_alias='currently_employed')
    substance_use: bool = Field(..., validation_alias='substance_use', serialization_alias='substance_use')
    time_unemployed: int = Field(..., validation_alias='time_unemployed', serialization_alias='time_unemployed')
    need_mental_health_support_bool: bool = Field(..., validation_alias='need_mental_health_support_bool', serialization_alias='need_mental_health_support_bool')

    # The following field serializer converts specific fields into numerical types,
    @field_serializer('income_source')
    def serialize_income_source(self, income_source: str):
        match income_source:
            case 'No Source of Income':
                return 1
            case 'Employment Insurance':
                return 2
            case 'Workplace Safety and Insurance Board':
                return 3
            case 'Ontario Works applied or receiving':
                return 4
            case 'Ontario Disability Support Program applied or receiving':
                return 5
            case 'Dependent of someone receiving OW or ODSP':
                return 6
            case 'Crown Ward':
                return 7
            case 'Employment':
                return 8
            case 'Self-Employment':
                return 9
            case 'Other (specify)':
                return 10

    @field_serializer('housing')
    def serialize_housing(self, housing: str):
        match housing:
            case 'Renting-private':
                return 1
            case 'Renting-subsidized':
                return 2
            case 'Boarding or lodging':
                return 3
            case 'Homeowner':
                return 4
            case 'Living with family/friend':
                return 5
            case 'Institution':
                return 6
            case 'Temporary second residence':
                return 7
            case 'Band-owned home':
                return 8
            case 'Homeless or transient':
                return 9
            case 'Emergency hostel':
                return 10

    @field_serializer('level_of_schooling')
    def serialize_level_of_schooling(self, level_of_schooling: str):
        match level_of_schooling:
            case 'Grade 0-8':
                return 1
            case 'Grade 9':
                return 2
            case 'Grade 10':
                return 3
            case 'Grade 11':
                return 4
            case 'Grade 12 or equivalent':
                return 5
            case 'OAC or Grade 13':
                return 6
            case 'Some college':
                return 7
            case 'Some university':
                return 8
            case 'Some apprenticeship':
                return 9
            case 'Certificate of Apprenticeship':
                return 10
            case 'Journeyperson':
                return 11
            case 'Certificate/Diploma':
                return 12
            case 'Bachelor’s degree':
                return 13
            case 'Post graduate':
                return 14

    @field_serializer('citizen_status')
    def serialize_citizen_status(self, citizen_status: str):
        match citizen_status:
            case 'citizen':
                return 0
            case 'permanent_resident':
                return 1
            case 'temporary_resident':
                return 2

    @field_serializer('gender')
    def serialize_age(self, gender: str):
        return 1 if gender == 'M' else 2
