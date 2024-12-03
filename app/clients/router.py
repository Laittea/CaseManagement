from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import os
import pandas as pd

from .service.logic import interpret_and_calculate
from .schema import PredictionInput
from .crud import create_user_in_db, get_all_user_data, get_user_by_id, update_user, delete_user

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

# create a user


@router.post("/create-user", response_class=JSONResponse)
async def create_user(data: PredictionInput):
    """
    API endpoint to create a user in the database.
    """
    try:
        create_user_in_db(data)
        return JSONResponse(
            content={"message": "User created successfully",
                     "user": data.dict()},
            status_code=201
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating user: {str(e)}"
        )

# Get user data


@router.get("/users", response_class=JSONResponse)
async def get_all_users():
    """
    API endpoint to retrieve all user data from the database.
    """
    try:
        users = get_all_user_data()
        if not users:
            return JSONResponse(
                content={"message": "No users found in the database."},
                status_code=200
            )
        keys = [
            "id", "age", "gender", "work_experience", "canada_workex", "dep_num",
            "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
            "reading_english_scale", "speaking_english_scale", "writing_english_scale",
            "numeracy_scale", "computer_scale", "transportation_bool", "caregiver_bool",
            "housing", "income_source", "felony_bool", "attending_school",
            "currently_employed", "substance_use", "time_unemployed",
            "need_mental_health_support_bool"
        ]

        users_list = [dict(zip(keys, user)) for user in users]

        return JSONResponse(content=users_list, status_code=200)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving users: {e}"
        )

# Get client by unique id


@router.get("/users/{user_id}", response_class=JSONResponse)
async def get_client(user_id: int):
    """
    API endpoint to retrieve a specific client by their unique ID from the database.
    """
    try:
        client_data = get_user_by_id(user_id)

        if not client_data:
            raise HTTPException(status_code=404, detail="Client not found")

        keys = [
            "id", "age", "gender", "work_experience", "canada_workex", "dep_num",
            "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
            "reading_english_scale", "speaking_english_scale", "writing_english_scale",
            "numeracy_scale", "computer_scale", "transportation_bool", "caregiver_bool",
            "housing", "income_source", "felony_bool", "attending_school",
            "currently_employed", "substance_use", "time_unemployed",
            "need_mental_health_support_bool"
        ]

        client_dict = dict(zip(keys, client_data))

        return JSONResponse(content=client_dict, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving user: {e}"
        )

# update user


@router.put("/users/{user_id}", response_class=JSONResponse)
async def update_user(user_id: int, updated_data: PredictionInput):
    """
    API endpoint to update a specific client's information by their unique ID.
    """
    try:
        existing_client = get_user_by_id(user_id)
        if not existing_client:
            raise HTTPException(status_code=404, detail="Client not found")

        update_status = update_user(user_id, updated_data)

        if not update_status:
            raise HTTPException(
                status_code=500, detail="Error updating user")

        return JSONResponse(
            content={
                "message": "User updated successfully",
                "updated_user_id": user_id
            },
            status_code=200
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error updating client: {e}"
        )


# Delete client


@router.delete("/users/{user_id}", response_class=JSONResponse)
async def delete_client(user_id: int):
    """
    API endpoint to delete a specific client by their unique ID.
    """
    try:
        client_data = get_user_by_id(user_id)

        if not client_data:
            raise HTTPException(status_code=404, detail="Client not found")

        delete_status = delete_user(user_id)
        if delete_status == 404:
            raise HTTPException(
                status_code=404, detail="Client not found during deletion")

        return JSONResponse(
            content={
                "message": "Client deleted successfully",
                "deleted_client": client_data
            },
            status_code=200
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting client: {e}"
        )
