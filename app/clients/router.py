from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import os
import pandas as pd

from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

# create a user
@router.post("/create-user", response_class=JSONResponse)
async def create_user(data: PredictionInput):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')   
        new_data = pd.DataFrame([data.dict()]) 
        new_data.to_csv(file_path, mode='a', index=False, header=False) 
        
        print("User created:", data.dict())
        return JSONResponse(content={"message": "User created successfully", "user": data.dict()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

# Get user data
@router.get("/read-csv", response_class=JSONResponse)
async def read_csv():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
        
        data = pd.read_csv(file_path)
        
        return data.head().to_dict(orient="records")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {e}")


async def load_csv():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(current_dir, 'service', 'data_commontool.csv')
    try:
        df = pd.read_csv(filename)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")

@router.get("/get-age", response_model=list)
async def get_age():
    df = await load_csv()
    if 'age' not in df.columns:
        raise HTTPException(status_code=404, detail="Column 'age' not found in CSV")
    return df['age'].tolist()

@router.get("/get-gender", response_model=list)
async def get_gender():
    df = await load_csv()
    if 'gender' not in df.columns:
        raise HTTPException(status_code=404, detail="Column 'gender' not found in CSV")
    return df['gender'].tolist()

@router.get("/get-born-place", response_model=list)
async def get_born_place():
    df = await load_csv()
    if 'canada_born' not in df.columns:
        raise HTTPException(status_code=404, detail="Column 'canada_born' not found in CSV")
    return df['canada_born'].tolist()