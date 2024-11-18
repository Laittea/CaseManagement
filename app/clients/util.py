import os
import json
from functools import lru_cache
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR

@lru_cache
def util_get_cols():
    """Read categorical columns from dotenv file."""
    load_dotenv()
    return json.loads(os.getenv('FEATURE_COLS_IN_SEQ'))


def get_model(model_type):
    """Dynamically load a machine learning model based on the configuration."""
    model_mapping = {
        "RandomForestRegressor": RandomForestRegressor,
        "LinearRegression": LinearRegression,
        "GradientBoostingRegressor": GradientBoostingRegressor,
        "SVR": SVR
    }
    if model_type not in model_mapping:
        raise ValueError(f"Unsupported model type: {model_type}. Choose from {list(model_mapping.keys())}")

    return model_mapping[model_type]()
