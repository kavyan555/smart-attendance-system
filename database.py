import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()


def get_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection



def insert_attendance(name):

    connection = get_connection()

    cursor = connection.cursor()

    # Prevent duplicate attendance for today
    check_query = """
    SELECT * FROM attendance
    WHERE name=%s
    AND attendance_date=CURDATE()
    """

    cursor.execute(check_query, (name,))

    existing = cursor.fetchone()

    if existing:

        cursor.close()

        connection.close()

        return
      
    insert_query = """
    INSERT INTO attendance
    (
        name,
        attendance_date,
        attendance_time,
        status
    )
    VALUES
    (
        %s,
        CURDATE(),
        CURTIME(),
        %s
    )
    """

    cursor.execute(
        insert_query,
        (
            name,
            "Present"
        )
    )

    connection.commit()

    cursor.close()

    connection.close()

def get_student_email(name):

    connection = get_connection()

    cursor = connection.cursor()

    query = """
    SELECT email
    FROM students
    WHERE name=%s
    """

    cursor.execute(query, (name,))

    result = cursor.fetchone()

    cursor.close()

    connection.close()

    if result:
        return result[0]

    return None