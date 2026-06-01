import cv2
import pickle
import numpy as np

from mtcnn import MTCNN
from keras_facenet import FaceNet

THRESHOLD = 0.75

embedder = FaceNet()

detector = MTCNN()

with open("embeddings/embeddings.pkl", "rb") as f:

    database = pickle.load(f)


# PREPROCESS FUNCTION
def preprocess_face(face):

    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

    face = cv2.resize(face, (160,160))

    face = face.astype("float32")

    return face

# RECOGNITION FUNCTION

def recognize_faces(frame):

    results = []

    detections = detector.detect_faces(frame)

    for detection in detections:

        confidence = detection['confidence']

        if confidence < 0.95:
            continue

        x, y, w, h = detection['box']

        x = max(0, x)
        y = max(0, y)

        face = frame[y:y+h, x:x+w]

        if face is None or face.size == 0:
            continue

        try:

            processed_face = preprocess_face(face)

            processed_face = np.expand_dims(
                processed_face,
                axis=0
            )

            current_embedding = embedder.embeddings(
                processed_face
            )[0]

        except:
            continue

        best_similarity = -1

        best_person = "Unknown"

        for person_name, embeddings in database.items():

            for saved_embedding in embeddings:

                similarity = np.dot(
                    current_embedding,
                    saved_embedding
                ) / (
                    np.linalg.norm(current_embedding)
                    * np.linalg.norm(saved_embedding)
                )

                if similarity > best_similarity:

                    best_similarity = similarity

                    best_person = person_name

        if best_similarity < THRESHOLD:

            best_person = "Unknown"

        results.append({
            "name": best_person,
            "box": (x, y, w, h)
        })

    return results