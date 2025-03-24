import pickle
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Model map for easy switching
MODEL_MAP = {
    "linear_regression": LinearRegression()
}

ALL_FEATURES = [
    'age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
    'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
    'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool', 'caregiver_bool',
    'housing', 'income_source', 'felony_bool', 'attending_school', 'currently_employed',
    'substance_use', 'time_unemployed', 'need_mental_health_support_bool',
    'employment_assistance', 'life_stabilization', 'retention_services', 'specialized_services',
    'employment_related_financial_supports', 'employer_financial_supports', 'enhanced_referrals'
]

LINEAR_MODEL_FEATURES = [
    'age', 'work_experience', 'canada_workex', 'level_of_schooling', 'fluent_english',
    'reading_english_scale', 'speaking_english_scale', 'writing_english_scale', 'numeracy_scale', 'computer_scale'
]


# Dynamically get the current script's directory (this will always work regardless of where you run from)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to CSV file using relative path
DATA_PATH = os.path.join(BASE_DIR, '../../clients/service/data_commontool_synthetic.csv')

# Path to output model directory
MODEL_DIR = os.path.join(BASE_DIR, '../../clients/service/MLmodels/')
os.makedirs(MODEL_DIR, exist_ok=True)  # auto create if not exists

def load_data(selected_features):
    data = pd.read_csv(DATA_PATH)
    X = np.array(data[selected_features])
    y = np.array(data['success_rate'])
    return X, y

def train_and_evaluate_with_split(model_name, selected_features):
    X, y = load_data(selected_features)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = MODEL_MAP[model_name]
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Hold-out Test Set - MAE: {mae:.2f} | MSE: {mse:.2f} | R2: {r2:.2f}")
    return model  # return model so you can save it later

def cross_validate_model(model_name, selected_features):
    X, y = load_data(selected_features)
    model = MODEL_MAP[model_name]
    cv = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-fold CV with shuffling
    r2_scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
    mae_scores = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_absolute_error")
    
    print(f"Cross-Validation R² scores: {r2_scores}")
    print(f"Mean R²: {np.mean(r2_scores):.3f}")
    print(f"Cross-Validation MAE scores: {mae_scores}")
    print(f"Mean MAE: {np.mean(mae_scores):.3f}")

def save_model(model, filename):
    model_path = os.path.join(MODEL_DIR, filename)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Model saved as {model_path}")

def main():
    print("=== Linear Regression on ALL_FEATURES ===")
    train_and_evaluate_with_split("linear_regression", ALL_FEATURES)
    cross_validate_model("linear_regression", ALL_FEATURES)
    
    print("\n=== Linear Regression on LINEAR_MODEL_FEATURES ===")
    model = train_and_evaluate_with_split("linear_regression", LINEAR_MODEL_FEATURES)
    cross_validate_model("linear_regression", LINEAR_MODEL_FEATURES)
    
    # Save model trained on linear subset
    save_model(model, "linear_model_subset.pkl")

if __name__ == "__main__":
    main()
