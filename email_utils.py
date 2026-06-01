import os
import smtplib

from dotenv import load_dotenv

from email.mime.text import MIMEText

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")

PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_email(
    student_name,
    receiver_email
):

    try:

        subject = "Attendance Marked"

        body = f"""
Hello {student_name},

Your attendance has been marked successfully.

Regards,
Smart Attendance System
"""

        msg = MIMEText(body)

        msg['Subject'] = subject

        msg['From'] = EMAIL

        msg['To'] = receiver_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL,
            PASSWORD
        )

        server.send_message(msg)

        server.quit()

        print(
            f"Email Sent -> {receiver_email}"
        )

    except Exception as e:

        print(
            "Email Error:",
            e
        )