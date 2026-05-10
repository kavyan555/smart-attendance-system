import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()


conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)

cursor = conn.cursor()


# =========================================
# INSERT ATTENDANCE
# =========================================

def insert_attendance(
    name,
    status,
    confidence,
    date,
    time
):

    query = """
    INSERT INTO attendance
    (name, status, date, time)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        name,
        status,
        date,
        time
    )

    cursor.execute(
        query,
        values
    )

    conn.commit()


# =========================================
# CHECK DUPLICATE
# =========================================

def already_marked(name, date):

    query = """
    SELECT *
    FROM attendance
    WHERE name=%s AND date=%s
    """

    cursor.execute(
        query,
        (name, date)
    )

    return cursor.fetchone() is not None