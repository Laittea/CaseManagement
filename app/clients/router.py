from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
import os
import pandas as pd

from .service.logic import interpret_and_calculate
from .schema import PredictionInput
from .crud import create_user, get_all_user_data, get_user_by_id, update_user, delete_user

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
        # Call the create_user function from crud.py
        create_user(data)
        return JSONResponse(
            content={"message": "User created successfully",
                     "user": data.dict()},
            status_code=201
        )
    except Exception as e:
        # Handle any exceptions raised during the creation process
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
        # Fetch all users from the database
        users = get_all_user_data()

        # Check if the database returned any users
        if not users:
            return JSONResponse(
                content={"message": "No users found in the database."},
                status_code=200
            )

        # Define the keys for the user dictionary
        keys = [
            "id", "age", "gender", "work_experience", "canada_workex", "dep_num",
            "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
            "reading_english_scale", "speaking_english_scale", "writing_english_scale",
            "numeracy_scale", "computer_scale", "transportation_bool", "caregiver_bool",
            "housing", "income_source", "felony_bool", "attending_school",
            "currently_employed", "substance_use", "time_unemployed",
            "need_mental_health_support_bool"
        ]

        # Convert the list of tuples into a list of dictionaries
        users_list = [dict(zip(keys, user)) for user in users]

        return JSONResponse(content=users_list, status_code=200)

    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving users: {e}"
        )

# Get specific client by unique identifier


@router.get("/users/{user_id}", response_class=JSONResponse)
async def get_client(user_id: int):
    """
    API endpoint to retrieve a specific client by their unique ID from the database.
    """
    try:
        # Fetch client data by ID from the database
        client_data = get_user_by_id(user_id)

        # If the client does not exist, raise a 404 error
        if not client_data:
            raise HTTPException(status_code=404, detail="Client not found")

        # Define the keys for the client dictionary
        keys = [
            "id", "age", "gender", "work_experience", "canada_workex", "dep_num",
            "canada_born", "citizen_status", "level_of_schooling", "fluent_english",
            "reading_english_scale", "speaking_english_scale", "writing_english_scale",
            "numeracy_scale", "computer_scale", "transportation_bool", "caregiver_bool",
            "housing", "income_source", "felony_bool", "attending_school",
            "currently_employed", "substance_use", "time_unemployed",
            "need_mental_health_support_bool"
        ]

        # Convert the tuple returned by get_user_by_id into a dictionary
        client_dict = dict(zip(keys, client_data))

        return JSONResponse(content=client_dict, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        # Handle unexpected errors
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
        # Check if the client exists before updating
        existing_client = get_user_by_id(user_id)
        if not existing_client:
            raise HTTPException(status_code=404, detail="Client not found")

        # Update the client information
        update_status = update_user(user_id, updated_data)

        # Check if the update was successful
        if not update_status:
            raise HTTPException(
                status_code=500, detail="Error updating user")

        # Return a success message
        return JSONResponse(
            content={
                "message": "User updated successfully",
                "updated_user_id": user_id
            },
            status_code=200
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error updating client: {e}"
        )


# Delete specific client


@router.delete("/users/{user_id}", response_class=JSONResponse)
async def delete_client(user_id: int):
    """
    API endpoint to delete a specific client by their unique ID.
    """
    try:
        # Retrieve client data before deletion
        client_data = get_user_by_id(user_id)

        # If the client does not exist, raise a 404 error
        if not client_data:
            raise HTTPException(status_code=404, detail="Client not found")

        # Perform the deletion
        delete_status = delete_user(user_id)

        # Check the deletion status
        if delete_status == 404:
            raise HTTPException(
                status_code=404, detail="Client not found during deletion")

        # Return the deleted client data (tuple)
        return JSONResponse(
            content={
                "message": "Client deleted successfully",
                "deleted_client": client_data
            },
            status_code=200
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting client: {e}"
        )


# from fastapi import APIRouter, HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.responses import JSONResponse
# import os
# import pandas as pd

# from .service.logic import interpret_and_calculate
# from .schema import PredictionInput

# router = APIRouter(prefix="/clients", tags=["clients"])

# @router.post("/predictions")
# async def predict(data: PredictionInput):
#     print("HERE")
#     print(data.model_dump())
#     return interpret_and_calculate(data.model_dump())

# # create a user
# @router.post("/create-user", response_class=JSONResponse)
# async def create_user(data: PredictionInput):
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
#         new_data = pd.DataFrame([data.dict()])
#         if os.path.exists(file_path):
#             # Add newline before appending if file is not empty
#             if os.path.getsize(file_path) > 0:
#                 with open(file_path, 'a', newline='') as f:
#                     new_data.to_csv(f, index=False, header=False)
#             else:
#                 # If file is empty, write with headers
#                 new_data.to_csv(file_path, index=False)
#         else:
#             # If file doesn't exist, create it with headers
#             new_data.to_csv(file_path, index=False)
#         print("User created:", data.dict())
#         return JSONResponse(content={"message": "User created successfully", "user": data.dict()})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

# # Get user data
# @router.get("/read-csv", response_class=JSONResponse)
# async def read_csv():
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')

#         data = pd.read_csv(file_path)

#         return data.head().to_dict(orient="records")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error reading CSV: {e}")


# # Get specific client by unique identifier
# @router.get("/client/{client_index}", response_class=JSONResponse)
# async def get_client(client_index: int):
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
#         data = pd.read_csv(file_path)

#         if client_index >= len(data):
#             raise HTTPException(status_code=404, detail="Client not found")

#         client_data = data.iloc[client_index].to_dict()
#         return JSONResponse(content=client_data)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving client: {e}")


# # Delete specific client
# @router.delete("/client/{client_index}", response_class=JSONResponse)
# async def delete_client(client_index: int):
#     try:
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         file_path = os.path.join(current_dir, 'service', 'data_commontool.csv')
#         df = pd.read_csv(file_path)

#         if client_index >= len(df):
#             raise HTTPException(status_code=404, detail="Client not found")

#         # Store client data before deletion for response
#         deleted_client = df.iloc[client_index].to_dict()

#         # Delete the client
#         df = df.drop(client_index)
#         df.to_csv(file_path, index=False)

#         return JSONResponse(
#             content={
#                 "message": "Client deleted successfully",
#                 "deleted_client": deleted_client
#             }
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error deleting client: {e}")

# async def load_csv():
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     filename = os.path.join(current_dir, 'service', 'data_commontool.csv')
#     try:
#         df = pd.read_csv(filename)
#         return df
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error reading CSV: {str(e)}")

# @router.get("/get-age", response_model=list)
# async def get_age():
#     df = await load_csv()
#     if 'age' not in df.columns:
#         raise HTTPException(status_code=404, detail="Column 'age' not found in CSV")
#     return df['age'].tolist()

# @router.get("/get-gender", response_model=list)
# async def get_gender():
#     df = await load_csv()
#     if 'gender' not in df.columns:
#         raise HTTPException(status_code=404, detail="Column 'gender' not found in CSV")
#     return df['gender'].tolist()

# @router.get("/get-born-place", response_model=list)
# async def get_born_place():
#     df = await load_csv()
#     if 'canada_born' not in df.columns:
#         raise HTTPException(status_code=404, detail="Column 'canada_born' not found in CSV")
#     return df['canada_born'].tolist()
