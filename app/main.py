from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from clients.router import router as clients_router

# from clients.schema import PredictionInput
# from clients.crud import create_user, get_all_user_data, get_user_by_id, update_user, delete_user
# from clients.db_setup import create_tables

from app.clients.router import router as clients_router
from app.clients.schema import PredictionInput
from app.clients.crud import create_user, get_all_user_data, get_user_by_id, update_user, delete_user
from app.clients.db_setup import create_tables

app = FastAPI()

# Set API endpoints on router
app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# # Sprint4- make sure database has been created
# create_tables()

# # insert data- create user
# new_user = PredictionInput(
#     age=25,
#     gender="Female",
#     work_experience=3,
#     canada_workex=1,
#     dep_num=1,
#     canada_born="No",
#     citizen_status="Citizen",
#     level_of_schooling="Master's",
#     fluent_english="Yes",
#     reading_english_scale=5,
#     speaking_english_scale=5,
#     writing_english_scale=4,
#     numeracy_scale=3,
#     computer_scale=4,
#     transportation_bool="Yes",
#     caregiver_bool="No",
#     housing="Apartment",
#     income_source="Employment",
#     felony_bool="No",
#     attending_school="No",
#     currently_employed="Yes",
#     substance_use="No",
#     time_unemployed=2,
#     need_mental_health_support_bool="Yes"
# )

# create_user(new_user)

# # Retrieve all users
# # print("\nFetching all users...")
# # users = get_all_user_data()
# # for user in users:
# #     print(user)

# # Retrieve a specific user by ID
# print("\nFetching user with ID 2...")
# user = get_user_by_id(2)
# if user:
#     print(user)
# else:
#     print("User not found.")

# # Update a user
# print("\nUpdating user with ID 2...")
# updated_user = PredictionInput(
#     age=50,
#     gender="Male",
#     work_experience=20,
#     canada_workex=5,
#     dep_num=2,
#     canada_born="No",
#     citizen_status="Citizen",
#     level_of_schooling="Master's",
#     fluent_english="Yes",
#     reading_english_scale=5,
#     speaking_english_scale=5,
#     writing_english_scale=5,
#     numeracy_scale=4,
#     computer_scale=5,
#     transportation_bool="Yes",
#     caregiver_bool="No",
#     housing="Own House",
#     income_source="Self-employed",
#     felony_bool="No",
#     attending_school="No",
#     currently_employed="Yes",
#     substance_use="No",
#     time_unemployed=0,
#     need_mental_health_support_bool="No"
# )
# if update_user(2, updated_user):
#     print("User updated successfully.")
# else:
#     print("Failed to update user.")

# # # Delete a user
# # print("\nDeleting user with ID 1...")
# # status = delete_user(2)
# # if status == 200:
# #     print("User deleted successfully.")
# # elif status == 404:
# #     print("User not found. Could not delete.")

# # # Attempt to fetch the deleted user
# # print("\nFetching user with ID 1 after deletion...")
# # user = get_user_by_id(2)
# # if user:
# #     print(user)
# # else:
# #     print("User not found.")
