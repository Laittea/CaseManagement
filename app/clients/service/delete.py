import sqlite3
from fastapi import HTTPException

DATABASE = '../mydatabase.db'

def check_valid_input(client_id):
    if not client_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid client_id format.")

# Deletion service logic
async def delete_client(client_id: str):
    # Validate input
    check_valid_input(client_id)
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Check if the client exists
        cursor.execute("SELECT * FROM CommonAssessmentTool_Table WHERE client_id = ?", (client_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(
                status_code=404,
                detail=f"Client with ID {client_id} not found"
            )

        # Delete the client
        cursor.execute("DELETE FROM CommonAssessmentTool_Table WHERE client_id = ?", (client_id,))
        conn.commit()

        return {
            "success": True,
            "message": f"Client {client_id} successfully deleted",
            "client_id": client_id
        }
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error occurred: {str(e)}"
        ) from e
    finally:
        conn.close()
