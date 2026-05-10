import streamlit as st
import cv2
import pickle
import pandas as pd
import plotly.express as px
import time

from datetime import datetime

from utils.face_detector import detect_faces
from utils.face_utils import preprocess_face
from utils.match_utils import match_face
from models.facenet_model import get_embedding
from utils.attendance_logic import mark_attendance

from database.db import conn


# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="🎓",
    layout="wide"
)


# =========================================
# LOAD EMBEDDINGS DATABASE
# =========================================

try:

    with open("embeddings/embeddings.pkl", "rb") as f:

        database = pickle.load(f)

except Exception as e:

    database = {}

    st.warning(
        f"No embeddings database found.\n{e}"
    )


# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fa;
    }

    .stButton button {
        border-radius: 10px;
        height: 45px;
        width: 100%;
        font-size: 16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🎓 Smart Attendance")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Daily Attendance",
        "Monthly Analytics",
        "Person-wise Analytics",
        "Live Camera"
    ]
)


# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

    st.title("🎓 Smart Attendance Dashboard")

    try:

        query = "SELECT * FROM attendance"

        df = pd.read_sql(query, conn)

        # FIX DATE
        df['date'] = pd.to_datetime(
            df['date']
        ).dt.date

        # FIX TIME
        df['time'] = df['time'].apply(
        lambda x: str(x).replace("0 days ", "")
        )

    except:

        df = pd.DataFrame()

    total_records = len(df)

    present_count = len(
        df[df['status'] == 'Present']
    ) if not df.empty else 0

    absent_count = len(
        df[df['status'] == 'Absent']
    ) if not df.empty else 0

    today = datetime.now().date()

    if not df.empty:

        today_df = df[
            df['date'] == today
        ]

    else:

        today_df = pd.DataFrame()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Records",
        total_records
    )

    col2.metric(
        "Present",
        present_count
    )

    col3.metric(
        "Absent",
        absent_count
    )

    col4.metric(
        "Today's Records",
        len(today_df)
    )

    st.divider()

    st.subheader("Recent Attendance")

    if not df.empty:

        latest_df = df.sort_values(
            by="date",
            ascending=False
        )

        st.dataframe(
            latest_df.head(10),
            hide_index=True,
            use_container_width=True
        )

    else:

        st.info(
            "No attendance records found."
        )


# =========================================
# DAILY ATTENDANCE
# =========================================

elif menu == "Daily Attendance":

    st.title("📅 Daily Attendance")

    try:

        query = """
        SELECT *
        FROM attendance
        ORDER BY date DESC
        """

        df = pd.read_sql(query, conn)

        # FIX DATE
        df['date'] = pd.to_datetime(
            df['date']
        ).dt.date

        # FIX TIME
        df['time'] = df['time'].apply(
            lambda x: str(x).replace("0 days ", "")
        )

        # DATE FILTER

        unique_dates = sorted(
            df['date'].unique(),
            reverse=True
        )

        selected_date = st.selectbox(
            "Select Date",
            unique_dates
        )

        filtered_df = df[
            df['date'] == selected_date
        ]

        # METRICS

        total_present = len(
            filtered_df[
                filtered_df['status'] == 'Present'
            ]
        )

        total_absent = len(
            filtered_df[
                filtered_df['status'] == 'Absent'
            ]
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Present",
            total_present
        )

        col2.metric(
            "Absent",
            total_absent
        )

        st.divider()

        st.dataframe(
            filtered_df,
            hide_index=True,
            use_container_width=True
        )

        csv = filtered_df.to_csv(
            index=False
        ).encode('utf-8')

        st.download_button(
            "⬇ Download CSV",
            csv,
            "attendance.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(
            f"Error loading attendance: {e}"
        )


# =========================================
# MONTHLY ANALYTICS
# =========================================

elif menu == "Monthly Analytics":

    st.title("📈 Monthly Analytics")

    try:

        query = """
        SELECT
            name,

            SUM(
                CASE
                    WHEN status='Present'
                    THEN 1
                    ELSE 0
                END
            ) as Present_Days,

            SUM(
                CASE
                    WHEN status='Absent'
                    THEN 1
                    ELSE 0
                END
            ) as Absent_Days

        FROM attendance

        GROUP BY name
        """

        df = pd.read_sql(query, conn)

        if not df.empty:

            total_present = df[
                'Present_Days'
            ].sum()

            total_absent = df[
                'Absent_Days'
            ].sum()

            col1, col2 = st.columns(2)

            col1.metric(
                "Total Present",
                total_present
            )

            col2.metric(
                "Total Absent",
                total_absent
            )

            st.divider()

            # BAR CHART

            fig1 = px.bar(
                df,
                x="name",
                y="Present_Days",
                text="Present_Days",
                color="name",
                title="Student-wise Present Count"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            st.divider()

            # PIE CHART

            fig2 = px.pie(
                df,
                names="name",
                values="Absent_Days",
                title="Absent Distribution"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        else:

            st.info(
                "No attendance data found."
            )

    except Exception as e:

        st.error(
            f"Analytics Error: {e}"
        )


# =========================================
# PERSON-WISE ANALYTICS
# =========================================

elif menu == "Person-wise Analytics":

    st.title("👤 Person-wise Analytics")

    try:

        query = """
        SELECT
            name,

            SUM(
                CASE
                    WHEN status='Present'
                    THEN 1
                    ELSE 0
                END
            ) as Present_Days,

            SUM(
                CASE
                    WHEN status='Absent'
                    THEN 1
                    ELSE 0
                END
            ) as Absent_Days

        FROM attendance

        GROUP BY name
        """

        df = pd.read_sql(query, conn)

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        if not df.empty:

            fig = px.pie(
                df,
                names='name',
                values='Present_Days',
                title="Attendance Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No attendance data found."
            )

    except Exception as e:

        st.error(f"Error: {e}")


# =========================================
# LIVE CAMERA
# =========================================

elif menu == "Live Camera":

    st.title("📷 Live AI Attendance Camera")

    st.info(
        """
        Instructions:
        - Face the camera properly
        - Avoid poor lighting
        - Stay stable for few seconds
        - Attendance is marked automatically
        """
    )

    run = st.checkbox(
        "Start Camera"
    )

    FRAME_WINDOW = st.image([])

    attendance_buffer = {}

    marked_students = set()

    BUFFER_THRESHOLD = 7

    if run:

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():

            st.error(
                "Unable to access camera."
            )

        else:

            st.success(
                "Camera Started"
            )

            while run:

                ret, frame = cap.read()

                if not ret:

                    st.error(
                        "Camera Error"
                    )

                    break

                faces = detect_faces(frame)

                for face in faces:

                    x1, y1, x2, y2 = face

                    face_crop = frame[
                        y1:y2,
                        x1:x2
                    ]

                    if face_crop is None:
                        continue

                    if face_crop.size == 0:
                        continue

                    if len(face_crop.shape) != 3:
                        continue

                    if (
                        face_crop.shape[0] < 50
                        or
                        face_crop.shape[1] < 50
                    ):
                        continue

                    try:

                        processed_face = preprocess_face(
                            face_crop
                        )

                        if processed_face is None:
                            continue

                        embedding = get_embedding(
                            processed_face
                        )

                        if embedding is None:
                            continue

                        matched_name, similarity = match_face(
                            embedding,
                            database
                        )

                        if matched_name != "Unknown":

                            if matched_name not in attendance_buffer:

                                attendance_buffer[
                                    matched_name
                                ] = 0

                            attendance_buffer[
                                matched_name
                            ] += 1

                            if attendance_buffer[
                                matched_name
                            ] >= BUFFER_THRESHOLD:

                                if matched_name not in marked_students:

                                    mark_attendance(
                                        matched_name,
                                        similarity
                                    )

                                    marked_students.add(
                                        matched_name
                                    )

                                    st.success(
                                        f"Attendance Marked: "
                                        f"{matched_name}"
                                    )

                            label = matched_name

                            color = (0, 255, 0)

                        else:

                            label = "Unknown"

                            color = (0, 0, 255)

                    except Exception as e:

                        print(
                            "LIVE CAMERA ERROR:",
                            e
                        )

                        label = "Face Error"

                        color = (255, 0, 0)

                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        color,
                        2
                    )

                    cv2.putText(
                        frame,
                        label,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )

                rgb_frame = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2RGB
                )

                FRAME_WINDOW.image(
                    rgb_frame,
                    channels="RGB"
                )

                time.sleep(0.03)

            cap.release()

            cv2.destroyAllWindows()

    else:

        st.warning(
            "Camera is stopped."
        )