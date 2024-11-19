from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import os
import pandas as pd

from .service.logic import interpret_and_calculate
from .schema import PredictionInput

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
        if os.path.exists(file_path):
            # Add newline before appending if file is not empty
            if os.path.getsize(file_path) > 0:
                with open(file_path, 'a', newline='') as f:
                    new_data.to_csv(f, index=False, header=False)
            else:
                # If file is empty, write with headers
                new_data.to_csv(file_path, index=False)
        else:
            # If file doesn't exist, create it with headers
            new_data.to_csv(file_path, index=False)
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


# Get specific client by unique identifier
@router.get("/client/{client_index}", response_class=JSONResponse)
async def get_client(client_index: int):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
        data = pd.read_csv(file_path)

        if client_index >= len(data):
            raise HTTPException(status_code=404, detail="Client not found")

        client_data = data.iloc[client_index].to_dict()
        return JSONResponse(content=client_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving client: {e}")


# # Update specific client information
# @router.put("/client/{client_index}", response_class=JSONResponse)
# async def update_client(client_index: int, data: PredictionInput):
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
#         df = pd.read_csv(file_path)
#
#         if client_index >= len(df):
#             raise HTTPException(status_code=404, detail="Client not found")
#
#         # Update the client data
#         df.iloc[client_index] = pd.Series(data.dict())
#         df.to_csv(file_path, index=False)
#
#         # Run updated prediction
#         updated_prediction = interpret_and_calculate(data.dict())
#
#         return JSONResponse(
#             content={
#                 "message": "Client updated successfully",
#                 "updated_data": data.dict(),
#                 "new_prediction": updated_prediction
#             }
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating client: {e}")


# Delete specific client
@router.delete("/client/{client_index}", response_class=JSONResponse)
async def delete_client(client_index: int):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
        df = pd.read_csv(file_path)

        if client_index >= len(df):
            raise HTTPException(status_code=404, detail="Client not found")

        # Store client data before deletion for response
        deleted_client = df.iloc[client_index].to_dict()

        # Delete the client
        df = df.drop(client_index)
        df.to_csv(file_path, index=False)

        return JSONResponse(
            content={
                "message": "Client deleted successfully",
                "deleted_client": deleted_client
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting client: {e}")

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