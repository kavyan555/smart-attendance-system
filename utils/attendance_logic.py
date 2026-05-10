from datetime import datetime

from database.db import (
    insert_attendance,
    already_marked
)

from utils.email_alerts import send_email


marked = set()


def mark_attendance(name, confidence=None):

    # IGNORE UNKNOWN
    if name == "Unknown":

        return False

    now = datetime.now()

    current_date = now.date()

    # BETTER TIME FORMAT
    current_time = now.strftime(
        "%H:%M:%S"
    )

    # PREVENT DUPLICATE MARKING
    if (
        name not in marked
        and
        not already_marked(
            name,
            current_date
        )
    ):

        insert_attendance(
            name,
            "Present",
            float(confidence)
            if confidence is not None
            else None,
            current_date,
            current_time
        )

        marked.add(name)

        # EMAIL ALERT
        try:

            send_email(
                name,
                current_time
            )

        except Exception as e:

            print(
                "EMAIL ERROR:",
                e
            )

        return True

    return False