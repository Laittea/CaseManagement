from http.client import HTTPException

from fastapi import APIRouter
from fastapi import HTTPException

from app.clients.schema import PredictionInput as Client
from app.clients.schema import ClientUpdate as DynamicClient
from app.clients.ConnectionManager import ConnectionManager
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

router = APIRouter(prefix="/clients", tags=["clients"])

# HEIHEIHEI
@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.get("/")
async def get_all():
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM clients"
        cursor.execute(query)
        clients = cursor.fetchall()
        cursor.close()

        if not clients:
            raise HTTPException(status_code=404, detail=f"No clients found")
        else:
            return clients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/{id}")
async def get_by_id(id: int):
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()

        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM clients WHERE client_id = {id}"
        cursor.execute(query)
        client = cursor.fetchone()

        cursor.close()
        connection_manager.close_connection(connection)

        if not client:
            raise HTTPException(status_code=404, detail=f"Client with id {id} not found")
        return client

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_client(client: Client):
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()

        cursor = connection.cursor(dictionary=True)
        query = """
        INSERT INTO clients (
            age, gender, work_experience, canada_workex, dep_num,
            canada_born, citizen_status, level_of_schooling, fluent_english,
            reading_english_scale, speaking_english_scale, writing_english_scale,
            numeracy_scale, computer_scale, transportation_bool, caregiver_bool,
            housing, income_source, felony_bool, attending_school,
            currently_employed, substance_use, time_unemployed, need_mental_health_support_bool
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        cursor.execute(query, (
            client.age, client.gender, client.work_experience, client.canada_workex,
            client.dep_num, client.canada_born, client.citizen_status, client.level_of_schooling,
            client.fluent_english, client.reading_english_scale, client.speaking_english_scale,
            client.writing_english_scale, client.numeracy_scale, client.computer_scale,
            client.transportation_bool, client.caregiver_bool, client.housing,
            client.income_source, client.felony_bool, client.attending_school,
            client.currently_employed, client.substance_use, client.time_unemployed,
            client.need_mental_health_support_bool
        ))
        connection.commit()
        cursor.close()
        connection_manager.close_connection(connection)
        return {"message": "Client created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Internal server error: {str(e)}")



@router.put("/{id}")
async def update_client(id: int, data: DynamicClient):
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()
        cursor = connection.cursor(dictionary=True)

        update_fields = []
        update_values = []
        for field, value in data.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            update_values.append(value)
        if not update_fields:
            raise HTTPException(status_code=400,
                                detail="No fields provided for update")
        update_values.append(id)
        query = f"""
               UPDATE clients
               SET {', '.join(update_fields)}
               WHERE client_id = %s
               """
        cursor.execute(query, tuple(update_values))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Client with id {id} not found")

        cursor.close()
        connection_manager.close_connection(connection)

        return {"message": f"Client id {id} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_client(id: int):
    try:
        connection_manager = ConnectionManager()
        connection = connection_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "DELETE FROM clients WHERE client_id = %s"
        cursor.execute(query, (id,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Client with id {id} not found")
        connection.commit()
        connection_manager.close_connection(connection)
        cursor.close()
        return {"message": "Client deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


