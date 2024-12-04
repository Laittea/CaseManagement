import sqlite3
import os

DB_FILE = "case_management.db"


def create_tables():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        work_experience INTEGER NOT NULL,
        canada_workex INTEGER NOT NULL,
        dep_num INTEGER NOT NULL,
        canada_born TEXT NOT NULL,
        citizen_status TEXT NOT NULL,
        level_of_schooling TEXT NOT NULL,
        fluent_english TEXT NOT NULL,
        reading_english_scale INTEGER NOT NULL,
        speaking_english_scale INTEGER NOT NULL,
        writing_english_scale INTEGER NOT NULL,
        numeracy_scale INTEGER NOT NULL,
        computer_scale INTEGER NOT NULL,
        transportation_bool TEXT NOT NULL,
        caregiver_bool TEXT NOT NULL,
        housing TEXT NOT NULL,
        income_source TEXT NOT NULL,
        felony_bool TEXT NOT NULL,
        attending_school TEXT NOT NULL,
        currently_employed TEXT NOT NULL,
        substance_use TEXT NOT NULL,
        time_unemployed INTEGER NOT NULL,
        need_mental_health_support_bool TEXT NOT NULL
    )
    ''')

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
