import cv2
import streamlit as st
import pandas as pd
import plotly.express as px

from recognition_core import recognize_faces

from database import (
    get_connection,
    insert_attendance,
    get_student_email
)

from email_utils import send_email


# PAGE CONFIG

st.set_page_config(
    page_title="Smart Attendance System",
    layout="wide"
)


# SIDEBAR

st.sidebar.title("🎓 Smart Attendance")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Live Camera",
        "Daily Attendance",
        "Monthly Analytics",
        "Person Analytics"
    ]
)


# DATABASE CONNECTION

connection = get_connection()


# DASHBOARD

if menu == "Dashboard":

    st.title("📊 Dashboard")

    attendance = pd.read_sql(
        "SELECT * FROM attendance ORDER BY id DESC",
        connection
    )

    # FIX TIME FORMAT

    attendance['attendance_time'] = attendance[
    'attendance_time'
    ].apply(
    lambda x: str(x).split()[-1]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        len(attendance)
    )

    col2.metric(
        "Unique Students",
        attendance['name'].nunique()
    )

    today_count = len(
        attendance[
            attendance['attendance_date']
            ==
            pd.Timestamp.today().date()
        ]
    )

    col3.metric(
        "Present Today",
        today_count
    )

    st.subheader("Recent Attendance")

    st.dataframe(
        attendance,
        use_container_width=True,
        hide_index=True
    )

# LIVE CAMERA

elif menu == "Live Camera":

    st.title("📷 Live Camera")

    run = st.checkbox("Start Camera")

    FRAME_WINDOW = st.image([])

    camera = cv2.VideoCapture(0)

    marked = set()

    while run:

        ret, frame = camera.read()

        if not ret:

            st.error("Camera Error")

            break

        results = recognize_faces(frame)

        for result in results:

            x, y, w, h = result['box']

            name = result['name']

            color = (0,255,0)

            if name == "Unknown":

                color = (0,0,255)
        
            # DRAW RECTANGLE
            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
                color,
                2
            )

            # SHOW NAME

            cv2.putText(
                frame,
                name,
                (x,y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            # ATTENDANCE

            if name != "Unknown":

                if name not in marked:

                    insert_attendance(name)

                    receiver_email = get_student_email(name)

                    if receiver_email:

                        try:

                            send_email(
                                name,
                                receiver_email
                            )

                            st.success(
                                f"Email sent to {name}"
                            )

                        except Exception as e:

                            st.error(
                                f"Email Error: {e}"
                            )

                    marked.add(name)

                    st.success(
                        f"Attendance Marked -> {name}"
                    )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        FRAME_WINDOW.image(frame)

    camera.release()


# DAILY ATTENDANCE

elif menu == "Daily Attendance":

    st.title("📅 Daily Attendance")

    attendance = pd.read_sql(
        "SELECT * FROM attendance ORDER BY attendance_date DESC",
        connection
    )

    attendance['attendance_time'] = attendance[
    'attendance_time'
     ].apply(
    lambda x: str(x).split()[-1]
    )


    attendance['attendance_date'] = pd.to_datetime(
        attendance['attendance_date']
    )

    dates = attendance['attendance_date'].dt.date.unique()

    selected_date = st.selectbox(
        "Select Date",
        dates
    )

    filtered = attendance[
        attendance['attendance_date'].dt.date
        ==
        selected_date
    ]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# MONTHLY ANALYTICS
elif menu == "Monthly Analytics":

    st.title("📈 Monthly Analytics")

    attendance = pd.read_sql(
        "SELECT * FROM attendance",
        connection
    )

    attendance['attendance_date'] = pd.to_datetime(
        attendance['attendance_date']
    )

    attendance['Month'] = attendance[
        'attendance_date'
    ].dt.strftime('%B')

    monthly_summary = attendance.groupby(
        'Month'
    ).size().reset_index(name='Attendance Count')

    month_order = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    monthly_summary['Month'] = pd.Categorical(
        monthly_summary['Month'],
        categories=month_order,
        ordered=True
    )

    monthly_summary = monthly_summary.sort_values(
        'Month'
    )

    chart = px.line(
        monthly_summary,
        x='Month',
        y='Attendance Count',
        markers=True,
        title='Monthly Attendance Trends'
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )
    



# PERSON ANALYTICS

elif menu == "Person Analytics":

    st.title("👤 Person Analytics")

    attendance = pd.read_sql(
        "SELECT * FROM attendance",
        connection
    )

    attendance['attendance_time'] = attendance[
    'attendance_time'
    ].apply(
    lambda x: str(x).split()[-1]
    )



    if attendance.empty:

        st.warning(
            "No attendance records found."
        )

        st.stop()

    person = st.selectbox(
        "Select Person",
        attendance['name'].unique()
    )

    filtered = attendance[
        attendance['name'] == person
    ]

    st.subheader(
        f"Attendance Records - {person}"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.metric(
        "Total Attendance",
        len(filtered)
    )

    filtered['attendance_date'] = pd.to_datetime(
        filtered['attendance_date']
    )

    chart = px.histogram(
        filtered,
        x="attendance_date",
        title=f"Attendance Analytics - {person}"
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )


# CLOSE DB CONNECTION

connection.close()