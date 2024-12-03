from fastapi import HTTPException
from app.clients.mapper import get_client

def check_valid_input(client_id):
    if not client_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid client_id format.")


async def retrieve_client(client_id: str):
    try:
        # Query the client
        client = get_client(client_id)
        if not client:
            raise HTTPException(
                status_code=404,
                detail=f"Client with ID {client_id} not found"
            )

        client_data = map_client_data(client)

        # Return the client data as JSON
        return client_data
    except Exception as e:
        raise e


def map_client_data(client: tuple) -> dict:
    columns = [
        "age", "gender", "work_experience", "canada_workex", "dep_num", "canada_born",
        "citizen_status", "level_of_schooling", "fluent_english", "reading_english_scale",
        "speaking_english_scale", "writing_english_scale", "numeracy_scale", "computer_scale",
        "transportation_bool", "caregiver_bool", "housing", "income_source", "felony_bool",
        "attending_school", "currently_employed", "substance_use", "time_unemployed",
        "need_mental_health_support_bool", "employment_assistance", "life_stabilization",
        "retention_services", "specialized_services", "employment_related_financial_supports",
        "employer_financial_supports", "enhanced_referrals", "success_rate", "client_id"
    ]
    return dict(zip(columns, client))
