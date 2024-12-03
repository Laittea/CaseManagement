import os
import sqlite3
from typing import Optional

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
        # Assuming update_data is a dict with column names as keys
        updates = ", ".join([f"{key} = ?" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(client_id)
        cursor.execute(f"UPDATE CommonAssessmentTool_Table SET {updates} WHERE client_id = ?", values)
        conn.commit()
    except sqlite3.Error as e:
        raise Exception(f"Database error occurred: {str(e)}") from e
    finally:
        conn.close()