import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Define feature set
FEATURES = [
    'age', 'gender', 'work_experience', 'canada_workex', 'dep_num', 'canada_born', 'citizen_status',
    'level_of_schooling', 'fluent_english', 'reading_english_scale', 'speaking_english_scale',
    'writing_english_scale', 'numeracy_scale', 'computer_scale', 'transportation_bool', 'caregiver_bool',
    'housing', 'income_source', 'felony_bool', 'attending_school', 'currently_employed',
    'substance_use', 'time_unemployed', 'need_mental_health_support_bool',
    'employment_assistance', 'life_stabilization', 'retention_services', 'specialized_services',
    'employment_related_financial_supports', 'employer_financial_supports', 'enhanced_referrals'
]

# Set relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '../data_commontool_synthetic.csv')
MODEL_DIR = os.path.join(BASE_DIR, '../final_MLmodels/')
os.makedirs(MODEL_DIR, exist_ok=True)

def load_data(selected_features):
    data = pd.read_csv(DATA_PATH)
    X = np.array(data[selected_features])
    y = np.array(data['success_rate'])
    return X, y

def build_pipeline():
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('ridge', RidgeCV(alphas=[0.01, 0.1, 1.0, 10.0, 100.0], cv=5))
    ])
    return pipeline

def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f"Hold-out Test Set - MAE: {mae:.2f} | MSE: {mse:.2f} | R2: {r2:.2f}")

def cross_validate(model, X, y):
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
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
    print(f"✅ Ridge model saved at {model_path}")

def main():
    X, y = load_data(FEATURES)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = build_pipeline()
    model.fit(X_train, y_train)
    
    evaluate_model(model, X_test, y_test)
    cross_validate(model, X, y)
    save_model(model, "final_ridge_model.pkl")

if __name__ == "__main__":
    main()
