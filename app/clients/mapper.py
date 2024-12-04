import os
import sqlite3
from typing import Optional
from app.clients.service.update_model import ClientUpdateModel

DATABASE = os.path.join(os.path.dirname(__file__), '../../mydatabase.db')

def get_client(client_id: str) -> Optional[tuple]:
    """
    Retrieve a client record from the database by client_id.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CommonAssessmentTool_Table WHERE client_id = ?", (client_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()

def get_all_clients_with_info(criteria):
    """
    Search for clients based on given criteria.

    :param criteria: A dictionary where keys are column names and values are the filter values.
    :return: A list of matching clients as dictionaries.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        if isinstance(criteria, ClientUpdateModel):
            client_dict = criteria.model_dump(exclude_unset=True)
        else:
            validated_data = ClientUpdateModel(**criteria)
            client_dict = validated_data.model_dump(exclude_unset=True)

        # Build the WHERE clause dynamically
        where_clauses = []
        values = []
        for key, value in client_dict.items():
            if value is not None:
                where_clauses.append(f"{key} = ?")
                values.append(value)

        where_statement = " AND ".join(where_clauses)
        if where_clauses:
            query = f"SELECT * FROM CommonAssessmentTool_Table WHERE {where_statement}"
        else:
            query = "SELECT * FROM CommonAssessmentTool_Table"

        cursor.execute(query, tuple(values))
        rows = cursor.fetchall()

        # Map each row to a dictionary
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
        return [dict(zip(columns, row)) for row in rows]
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()

def delete_client_from_db(client_id: str):
    """
    Delete a client record from the database by client_id.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM CommonAssessmentTool_Table WHERE client_id = ?", (client_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()

def update_client_in_db(client_id: str, update_data: dict):
    """Update a client record in the database by client_id."""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # If update_data is already a ClientUpdateModel, convert it to a dict
        if isinstance(update_data, ClientUpdateModel):
            update_dict = update_data.model_dump(exclude_unset=True)
        else:
            # If it's a dict, validate it first
            validated_data = ClientUpdateModel(**update_data)
            update_dict = validated_data.model_dump(exclude_unset=True)
        # Assuming update_data is a dict with column names as keys
        updates = ", ".join([f"{key} = ?" for key in update_dict.keys()])
        values = list(update_dict.values())
        values.append(client_id)
        cursor.execute(f"UPDATE CommonAssessmentTool_Table SET {updates} WHERE client_id = ?", values)
        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()

def create_client_in_db(client_data: ClientUpdateModel) -> int:
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if isinstance(client_data, ClientUpdateModel):
            client_dict = client_data.model_dump(exclude_unset=True)
        else:
            validated_data = ClientUpdateModel(**client_data)
            client_dict = validated_data.model_dump(exclude_unset=True)

        columns = ", ".join(client_dict.keys())
        placeholders = ", ".join(["?"] * len(client_dict))
        values = list(client_dict.values())

        cursor.execute(
            f"INSERT INTO CommonAssessmentTool_Table ({columns}) VALUES ({placeholders})",
            values
        )
        conn.commit()

        # Retrieve the last inserted row's ID (autoincremented client_id)
        return cursor.lastrowid
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()
