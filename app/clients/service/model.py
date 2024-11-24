"""
This module prepares and trains a machine learning model using the dataset,
and saves the trained model for future use.
"""

import pandas as pd


def prepare_models():
    """
    Prepares and trains a RandomForestRegressor model using the dataset.
    """
    # Load dataset and define the features and labels
    backend_code = pd.read_csv('data_commontool.csv')  # Variable renamed to snake_case
    # Define categorical columns and interventions
    categorical_cols = [
        'age',
        'gender',  # bool
        'work_experience',  # years of work experience
        'canada_workex',  # years of work experience in Canada
        'dep_num',  # number of dependents
        'canada_born',  # born in Canada
        'citizen_status',  # citizen status
        'level_of_schooling',  # highest level achieved (1-14)
        'fluent_english',  # English level fluency, scale (1-10)
        'reading_english_scale',  # reading scale (1-10)
        'speaking_english_scale',  # speaking level comfort (1-10)
        'writing_english_scale',  # writing scale (1-10)
        'numeracy_scale',  # numeracy scale (1-10)
        'computer_scale',  # computer use scale (1-10)
        'transportation_bool',  # need transportation support (bool)
        'caregiver_bool',  # is a primary caregiver (bool)
        'housing',  # housing situation (1-10)
        'income_source',  # source of income (1-10)
        'felony_bool',  # has a felony (bool)
        'attending_school',  # currently a student (bool)
        'currently_employed',  # currently employed (bool)
        'substance_use',  # disorder (bool)
        'time_unemployed',  # number of years unemployed
        'need_mental_health_support_bool',  # need support
    ]

    interventions = [
        'employment_assistance',
        'life_stabilization',
        'retention_services',
        'specialized_services',
        'employment_related_financial_supports',
        'employer_financial_supports',
        'enhanced_referrals',
    ]
    categorical_cols.extend(interventions)

    # Prepare training data
    x_categorical_baseline = backend_code[categorical_cols]  # Variable renamed to snake_case
    x_categorical_baseline
