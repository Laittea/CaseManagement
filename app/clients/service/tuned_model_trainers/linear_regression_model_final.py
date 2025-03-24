import pickle
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../data_commontool_synthetic.csv')
MODEL_DIR = os.path.join(BASE_DIR, '../final_MLmodels/')
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data(selected_features):
    data = pd.read_csv(DATA_PATH)
    X = np.array(data[selected_features])
    y = np.array(data['success_rate'])
    return X, y

def build_pipeline(use_poly=False):
    steps = [('scaler', StandardScaler())]
    if use_poly:
        steps.append(('poly', PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)))
    steps.append(('regressor', MODEL_MAP["linear_regression"]))
    return Pipeline(steps)

def train_and_evaluate_with_split(selected_features, use_poly=False):
    X, y = load_data(selected_features)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline = build_pipeline(use_poly=use_poly)
    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Hold-out Test Set - MAE: {mae:.2f} | MSE: {mse:.2f} | R2: {r2:.2f}")
    return pipeline

def cross_validate_model(selected_features, use_poly=False):
    X, y = load_data(selected_features)
    pipeline = build_pipeline(use_poly=use_poly)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    r2_scores = cross_val_score(pipeline, X, y, cv=cv, scoring="r2")
    mae_scores = -cross_val_score(pipeline, X, y, cv=cv, scoring="neg_mean_absolute_error")
    
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
    print("=== Linear Regression on ALL_FEATURES (+ poly) ===")
    model = train_and_evaluate_with_split(ALL_FEATURES, use_poly=True)
    cross_validate_model(ALL_FEATURES, use_poly=True)
    
    print("\n=== Linear Regression on LINEAR_MODEL_FEATURES ===")
    model_subset = train_and_evaluate_with_split(LINEAR_MODEL_FEATURES, use_poly=False)
    cross_validate_model(LINEAR_MODEL_FEATURES, use_poly=False)
    
    save_model(model_subset, "final_linear_model_subset.pkl")

if __name__ == "__main__":
    main()
