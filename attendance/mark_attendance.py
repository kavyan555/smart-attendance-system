from datetime import datetime
from database.db import insert_attendance, already_marked
from utils.email_alerts import send_email

def mark(name):
    now = datetime.now()

    if not already_marked(name, now.date()):
        insert_attendance(name, now.date(), now.time())
        print(f"{name} marked present")

        # SEND EMAIL
        send_email(name, now.time())