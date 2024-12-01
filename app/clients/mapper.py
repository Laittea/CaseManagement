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
