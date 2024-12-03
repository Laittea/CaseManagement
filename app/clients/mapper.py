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

