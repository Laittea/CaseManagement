from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from app.database import get_db
from app.models import Client
from sqlalchemy.orm import Session  # ✅ add this!
import numpy as np


router = APIRouter(prefix="/model", tags=["Model Management"])
def load_client_training_data(db):
    """
    Fetches client records and extracts features and labels for ML training.
    You can define your own target for now. We'll use 'currently_employed' as an example label.
    """
    clients = db.query(Client).all()
    X = []
    y = []

    for c in clients:
        try:
            features = [
                c.age or 0,
                c.gender or 0,
                c.work_experience or 0,
                c.canada_workex or 0,
                c.dep_num or 0,
                c.reading_english_scale or 0,
                c.speaking_english_scale or 0,
                c.writing_english_scale or 0,
                c.numeracy_scale or 0,
                c.computer_scale or 0,
            ]
            label = 1 if c.currently_employed else 0
            X.append(features)
            y.append(label)
        except:
            continue  # skip bad records

    return X, y

class ModelManager:
    available_models = {
        "logistic_regression": LogisticRegression(),
        "random_forest": RandomForestClassifier(),
        "neural_network": MLPClassifier()
    }

    current_model_name = "logistic_regression"
    current_model = available_models[current_model_name]

    @classmethod
    def set_model(cls, model_name: str):
        if model_name not in cls.available_models:
            raise ValueError("Model not found")
        cls.current_model_name = model_name
        cls.current_model = cls.available_models[model_name]

    @classmethod
    def get_current_model(cls) -> str:
        return cls.current_model_name

    @classmethod
    def list_models(cls):
        return list(cls.available_models.keys())

    @classmethod
    def predict(cls, input_data: list):
        try:
            return cls.current_model.predict(np.array(input_data).reshape(1, -1)).tolist()
        except Exception as e:
            return str(e)

    @router.post("/train_models")
    def train_models(db: Session = Depends(get_db)):
        X, y = load_client_training_data(db)

        if len(X) == 0:
            return {"error": "No training data found in the database."}

        for model in ModelManager.available_models.values():
            model.fit(X, y)

        return {
            "message": f"Trained {len(ModelManager.available_models)} models on {len(X)} samples."
        }

class SetModelRequest(BaseModel):
    model_name: str

@router.post("/set_model")
def set_model(request: SetModelRequest):
    try:
        ModelManager.set_model(request.model_name)
        return {"message": f"Switched to model: {request.model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class PredictRequest(BaseModel):
    input: list  # Example: [1, 0]

@router.post("/predict")
def predict(request: PredictRequest):
    prediction = ModelManager.predict(request.input)
    return {"input": request.input, "prediction": prediction}

class ModelSwitchRequest(BaseModel):
    model_name: str


@router.post("/set_model")
def set_model(request: ModelSwitchRequest):
    try:
        ModelManager.set_model(request.model_name)
        return {"message": f"Switched to model: {request.model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/current_model")
def current_model():
    return {"current_model": ModelManager.get_current_model()}


@router.get("/list_models")
def list_models():
    return {"available_models": ModelManager.list_models()}

