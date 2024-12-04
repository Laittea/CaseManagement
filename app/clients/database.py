import sqlite3

def get_db_connection():
    conn = sqlite3.connect('clients.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_clients_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            gender INTEGER,
            work_experience INTEGER,
            canada_workex INTEGER,
            dep_num INTEGER,
            canada_born INTEGER,
            citizen_status INTEGER,
            level_of_schooling INTEGER,
            fluent_english INTEGER,
            reading_english_scale INTEGER,
            speaking_english_scale INTEGER,
            writing_english_scale INTEGER,
            numeracy_scale INTEGER,
            computer_scale INTEGER,
            transportation_bool INTEGER,
            caregiver_bool INTEGER,
            housing INTEGER,
            income_source INTEGER,
            felony_bool INTEGER,
            attending_school INTEGER,
            currently_employed INTEGER,
            substance_use INTEGER,
            time_unemployed INTEGER,
            need_mental_health_support_bool INTEGER
        )
    ''')
    conn.commit()
    conn.close()