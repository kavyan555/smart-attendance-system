import cv2
import pickle
from ultralytics import YOLO

from utils.face_utils import preprocess_face
from utils.match_utils import match_face
from models.facenet_model import get_embedding
from attendance.mark_attendance import mark

from collections import Counter

# Stability buffer
recent_predictions = []

def get_stable_name(new_name):
    recent_predictions.append(new_name)

    if len(recent_predictions) > 5:
        recent_predictions.pop(0)

    most_common = Counter(recent_predictions).most_common(1)[0][0]
    return most_common


# Prevent duplicate attendance marking
marked = set()

# Load YOLO model
yolo = YOLO("yolov8n.pt")

# Load embeddings
with open("embeddings/embeddings.pkl", "rb") as f:
    database = pickle.load(f)

# Start webcam
cap = cv2.VideoCapture(0)

print("✅ Camera started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo(frame)[0]

    for box in results.boxes:
        cls = int(box.cls[0])

        # Only detect person (class 0)
        if cls != 0:
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # ✅ FIXED cropping
        face = frame[y1:y2, x1:x2]

        # Skip invalid faces
        if face.size == 0:
            continue

        # Preprocess & get embedding
        face_tensor = preprocess_face(face)
        emb = get_embedding(face_tensor)

        # Match face
        name = match_face(emb, database)

        # Stabilize prediction
        name = get_stable_name(name)

        # Mark attendance only once
        if name != "Unknown" and name not in marked:
            mark(name)
            marked.add(name)

        # Draw bounding box + name
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Smart Attendance", frame)

    # Press ESC to exit
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()