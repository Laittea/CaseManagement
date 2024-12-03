import sqlite3
from .schema import PredictionInput

DB_FILE = "case_management.db"


def create_user_in_db(data: PredictionInput):
    """
    insert user data to database
    """
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO users (
        age, gender, work_experience, canada_workex, dep_num, canada_born,
        citizen_status, level_of_schooling, fluent_english, reading_english_scale,
        speaking_english_scale, writing_english_scale, numeracy_scale, computer_scale,
        transportation_bool, caregiver_bool, housing, income_source, felony_bool,
        attending_school, currently_employed, substance_use, time_unemployed,
        need_mental_health_support_bool
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.age, data.gender, data.work_experience, data.canada_workex, data.dep_num, data.canada_born,
        data.citizen_status, data.level_of_schooling, data.fluent_english, data.reading_english_scale,
        data.speaking_english_scale, data.writing_english_scale, data.numeracy_scale, data.computer_scale,
        data.transportation_bool, data.caregiver_bool, data.housing, data.income_source, data.felony_bool,
        data.attending_school, data.currently_employed, data.substance_use, data.time_unemployed,
        data.need_mental_health_support_bool
    ))

    connection.commit()
    connection.close()

    print("User created successfully.")


def get_all_user_data():
    """
    Get all users from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    user_list = cur.fetchall()

    conn.close()
    return user_list


def get_user_by_id(uid: int):
    """
    Get a user's information using their ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute('SELECT * FROM users WHERE id = ?', (uid,))
    user_info = cur.fetchone()

    conn.close()

    if user_info:
        return user_info
    else:
        print(f"No user found with ID {uid}")
        return None


def update_user(uid: int, user_data: PredictionInput):
    """
    Update user information based on their ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Check if the user ID exists
    cur.execute('SELECT id FROM users WHERE id = ?', (uid,))
    user_exists = cur.fetchone()

    if not user_exists:
        print(f"User with ID {uid} does not exist. Update aborted.")
        conn.close()
        return False

    # update if the user exists
    cur.execute('''
    UPDATE users
    SET age = ?, gender = ?, work_experience = ?, canada_workex = ?, dep_num = ?,
        canada_born = ?, citizen_status = ?, level_of_schooling = ?, fluent_english = ?,
        reading_english_scale = ?, speaking_english_scale = ?, writing_english_scale = ?,
        numeracy_scale = ?, computer_scale = ?, transportation_bool = ?, caregiver_bool = ?,
        housing = ?, income_source = ?, felony_bool = ?, attending_school = ?,
        currently_employed = ?, substance_use = ?, time_unemployed = ?, need_mental_health_support_bool = ?
    WHERE id = ?
    ''', (
        user_data.age, user_data.gender, user_data.work_experience, user_data.canada_workex, user_data.dep_num,
        user_data.canada_born, user_data.citizen_status, user_data.level_of_schooling, user_data.fluent_english,
        user_data.reading_english_scale, user_data.speaking_english_scale, user_data.writing_english_scale,
        user_data.numeracy_scale, user_data.computer_scale, user_data.transportation_bool, user_data.caregiver_bool,
        user_data.housing, user_data.income_source, user_data.felony_bool, user_data.attending_school,
        user_data.currently_employed, user_data.substance_use, user_data.time_unemployed,
        user_data.need_mental_health_support_bool, uid
    ))

    conn.commit()
    conn.close()

    print(f"User with ID {uid} has been updated successfully.")
    return True


def delete_user(uid: int):
    """
    Delete a user by their ID. Check if the user ID exists; if not, return 404.
    """
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute('SELECT id FROM users WHERE id = ?', (uid,))
    user_exists = cur.fetchone()

    if not user_exists:
        conn.close()
        print(f"User with ID {uid} not found. Returning 404.")
        return 404

    cur.execute('DELETE FROM users WHERE id = ?', (uid,))
    conn.commit()
    conn.close()

    print(f"User with ID {uid} has been deleted successfully.")
    return 200
