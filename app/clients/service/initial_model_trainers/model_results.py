import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

models = [
    '../MLmodels/linear_model_subset.pkl',
    '../MLmodels/ridge_model.pkl',
    '../MLmodels/xgboost_model.pkl',
    '../MLmodels/model.pkl'
]

# Load data
# data = pd.read_csv('../data_commontool_synthetic.csv')
data = pd.read_csv('../data_commontool_synthetic_testdata.csv')

# Feature set for linear_model_subset.pkl
LINEAR_MODEL_FEATURES = [
    'age', 'work_experience', 'canada_workex', 'level_of_schooling', 'fluent_english',
    'reading_english_scale', 'speaking_english_scale', 'writing_english_scale', 'numeracy_scale', 'computer_scale'
]

# Targets
y = data['success_rate'].values

def load_model(filename):
    with open(filename, "rb") as model_file:
        return pickle.load(model_file)

def main():
    print("========== Starting model testing ==========\n")
    for model_path in models:
        loaded_model = load_model(model_path)
        model_name = model_path.split('/')[-1]
        print(f">>> Testing Model: {model_name}")
        
        # Choose feature set depending on model
        if 'linear_model_subset' in model_path:
            X = data[LINEAR_MODEL_FEATURES].values
        else:
            X = data.drop(columns=['success_rate']).values

        predictions = loaded_model.predict(X)
        mae = mean_absolute_error(y, predictions)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)
        print(f"    MAE: {mae:.2f}")
        print(f"    MSE: {mse:.2f}")
        print(f"    R2:  {r2:.2f}")
        print("-" * 40)
        
    print("\n========== Model testing completed ==========")

if __name__ == "__main__":
    main()
