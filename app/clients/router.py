from fastapi import APIRouter, HTTPException
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput
from app.clients.database import get_db_connection

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.post("/add")
async def add(data: PredictionInput):
    # Input data to SQLite
    conn = get_db_connection()
    conn.execute('''INSERT INTO clients 
                (age, gender, work_experience, canada_workex, dep_num, canada_born,
                citizen_status, level_of_schooling, fluent_english, reading_english_scale,
                speaking_english_scale, writing_english_scale, numeracy_scale, computer_scale,
                transportation_bool, caregiver_bool, housing, income_source, felony_bool,
                attending_school, currently_employed, substance_use, time_unemployed,
                need_mental_health_support_bool)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
            (data.age, data.gender, data.work_experience, data.canada_workex, data.dep_num, data.canada_born,
            data.citizen_status, data.level_of_schooling, data.fluent_english, data.reading_english_scale,
            data.speaking_english_scale, data.writing_english_scale, data.numeracy_scale, data.computer_scale,
            data.transportation_bool, data.caregiver_bool, data.housing, data.income_source, data.felony_bool,
            data.attending_school, data.currently_employed, data.substance_use, data.time_unemployed,
            data.need_mental_health_support_bool))
    conn.commit()
    client_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return { "client_id": client_id, 
        "prediction_result": interpret_and_calculate(data.model_dump())}

# get client by id
@router.get("/{client_id}")
async def get_client(client_id: int):
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
    conn.close()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return dict(client)

# update clients info by id
@router.put("/update/{client_id}")
async def update_client(client_id: int, data: PredictionInput):
    conn = get_db_connection()
    
    client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
    if client is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    
    conn.execute('''
        UPDATE clients
        SET age = ?, gender = ?, work_experience = ?, canada_workex = ?, dep_num = ?,
            canada_born = ?, citizen_status = ?, level_of_schooling = ?, fluent_english = ?,
            reading_english_scale = ?, speaking_english_scale = ?, writing_english_scale = ?,
            numeracy_scale = ?, computer_scale = ?, transportation_bool = ?, caregiver_bool = ?,
            housing = ?, income_source = ?, felony_bool = ?, attending_school = ?,
            currently_employed = ?, substance_use = ?, time_unemployed = ?, need_mental_health_support_bool = ?
        WHERE id = ?
        ''', (
            data.age, data.gender, data.work_experience, data.canada_workex, data.dep_num,
            data.canada_born, data.citizen_status, data.level_of_schooling, data.fluent_english,
            data.reading_english_scale, data.speaking_english_scale, data.writing_english_scale,
            data.numeracy_scale, data.computer_scale, data.transportation_bool, data.caregiver_bool,
            data.housing, data.income_source, data.felony_bool, data.attending_school,
            data.currently_employed, data.substance_use, data.time_unemployed,
            data.need_mental_health_support_bool, client_id
    ))
    
    conn.commit()
    conn.close()
    
    return {"message": "Client information updated successfully", "client_id": client_id}

# delete clients info by id
@router.delete("/delete/{client_id}")
async def delete_client(client_id: int):
    conn = get_db_connection()
    
    client = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,)).fetchone()
    if client is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    
    conn.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()

    return {"message": f"Client with id {client_id} deleted successfully."}