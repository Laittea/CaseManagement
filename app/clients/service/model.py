import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from app.clients.util import util_get_cols


def prepare_models():
    # Load dataset and define the features and labels
    backendCode = pd.read_csv('data_commontool.csv')
    # Define categorical columns and interventions
    # the order of features MUST be the same as the features when predicting the result in logic.py
    categorical_cols = util_get_cols()
    interventions = [
        'employment_assistance',
        'life_stabilization',
        'retention_services',
        'specialized_services',
        'employment_related_financial_supports',
        'employer_financial_supports',
        'enhanced_referrals'
    ]
    categorical_cols.extend(interventions)
    # Prepare training data
    X_categorical_baseline = backendCode[categorical_cols]
    y_baseline = backendCode['success_rate']
    X_categorical_baseline = np.array(X_categorical_baseline)
    y_baseline = np.array(y_baseline)
    X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline = train_test_split(
        X_categorical_baseline, y_baseline, test_size=0.2, random_state=42)

    rf_model_baseline = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_baseline.fit(X_train_baseline, y_train_baseline)

    # Example: Predicting on the test set
    baseline_predictions = rf_model_baseline.predict(X_test_baseline)

    
    return rf_model_baseline


#################### Test Data and Methods ####################

# original order of columns:
test_original_cols = ['age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
                      'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
                      'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool',
                      'caregiver_bool', 'housing', 'income_source', 'felony_bool', 'attending_school',
                      'currently_employed', 'substance_use', 'time_unemployed', 'need_mental_health_support_bool']


def test_column_order():
    print("\n#################### test_data_type_conversion() ####################")
    cols = util_get_cols()
    # print(cols)
    if cols == test_original_cols:
        print("PASS")
    else:
        print("FAIL")


def main():
    print("Start model.")
    model = prepare_models()

    pickle.dump(model, open("model.pkl", "wb")) #saves model to the file name input, write binary
    model = pickle.load(open("model.pkl", "rb")) #read binary


if __name__ == "__main__":
    main()
