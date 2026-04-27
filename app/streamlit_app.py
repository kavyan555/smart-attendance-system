import streamlit as st
import cv2
import pickle
import pandas as pd
import mysql.connector
from ultralytics import YOLO
from collections import Counter

from utils.face_utils import preprocess_face
from utils.match_utils import match_face
from models.facenet_model import get_embedding
from attendance.mark_attendance import mark

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ------------------------
# LOAD ENV (optional)
# ------------------------
from dotenv import load_dotenv
load_dotenv()

# ------------------------
# DB CONNECTION
# ------------------------
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
    auth_plugin='mysql_native_password'
)

# ------------------------
# LOAD MODELS
# ------------------------
yolo = YOLO("yolov8n.pt")

with open("embeddings/embeddings.pkl", "rb") as f:
    database = pickle.load(f)

# ------------------------
# UI SETUP
# ------------------------
st.set_page_config(page_title="Smart Attendance", layout="wide")
st.title("🎓 Smart Attendance System")

run = st.checkbox("Start Camera")

col1, col2 = st.columns(2)
frame_placeholder = col1.empty()
status_placeholder = col2.empty()

# Stability buffer
recent_predictions = []

def get_stable_name(new_name):
    recent_predictions.append(new_name)
    if len(recent_predictions) > 5:
        recent_predictions.pop(0)
    return Counter(recent_predictions).most_common(1)[0][0]

# Prevent duplicate marking
marked = set()

# ------------------------
# CAMERA LOOP
# ------------------------
if run:
    cap = cv2.VideoCapture(0)
    st.success("✅ Camera started")

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        results = yolo(frame)[0]
        detected_name = "No Face"

        for box in results.boxes:
            cls = int(box.cls[0])

            # Only detect person
            if cls != 0:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # ✅ FIXED cropping
            face = frame[y1:y2, x1:x2]

            if face.size == 0:
                continue

            face_tensor = preprocess_face(face)
            emb = get_embedding(face_tensor)

            name = match_face(emb, database)
            name = get_stable_name(name)

            if name != "Unknown" and name not in marked:
                mark(name)
                marked.add(name)

            detected_name = name

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, name, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame)

        status_placeholder.markdown(f"### 👤 Detected: {detected_name}")

    cap.release()

# ------------------------
# 📋 TODAY ATTENDANCE
# ------------------------
st.subheader("📅 Today's Attendance")

query_today = """
SELECT * FROM attendance
WHERE date = CURDATE()
"""

df_today = pd.read_sql(query_today, conn)
st.dataframe(df_today)

# ------------------------
# 👤 PERSON-WISE COUNT
# ------------------------
st.subheader("👤 Person-wise Attendance")

query_count = """
SELECT name, COUNT(*) as total_present
FROM attendance
GROUP BY name
"""

df_count = pd.read_sql(query_count, conn)
st.dataframe(df_count)
st.bar_chart(df_count.set_index("name"))

# ------------------------
# 📈 MONTHLY ANALYTICS
# ------------------------
st.subheader("📈 Monthly Analytics")

query_month = """
SELECT name, COUNT(*) as present_days
FROM attendance
WHERE MONTH(date) = MONTH(CURDATE())
GROUP BY name
"""

df_month = pd.read_sql(query_month, conn)

TOTAL_DAYS = 5  # adjust based on your dataset

df_month["absent_days"] = TOTAL_DAYS - df_month["present_days"]
df_month["attendance_%"] = (df_month["present_days"] / TOTAL_DAYS) * 100

st.dataframe(df_month)
st.bar_chart(df_month.set_index("name")[["present_days", "absent_days"]])