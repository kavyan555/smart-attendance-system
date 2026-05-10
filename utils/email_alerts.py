import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")


EMAILS = {
    "Kavya": "lkm83256@gmail.com"
}


def send_email(name, time):

    receiver = EMAILS.get(name)

    if not receiver:
        return

    subject = "Attendance Marked"

    body = f"{name} marked present at {time}"

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        print("Email Sent")

    except Exception as e:
        print(e)