import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kn@180597",  # 🔥 change this
    database="attendance_db"
)

cursor = conn.cursor()

def insert_attendance(name, date, time):
    query = "INSERT INTO attendance (name, date, time) VALUES (%s, %s, %s)"
    values = (name, date, time)

    cursor.execute(query, values)
    conn.commit()

def already_marked(name, date):
    query = "SELECT * FROM attendance WHERE name=%s AND date=%s"
    cursor.execute(query, (name, date))
    return cursor.fetchone() is not None