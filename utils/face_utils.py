import cv2
import numpy as np


def preprocess_face(face):

    try:

        face = cv2.cvtColor(
            face,
            cv2.COLOR_BGR2RGB
        )

        face = cv2.resize(
            face,
            (160, 160)
        )

        face = face.astype("float32")

        mean = face.mean()
        std = face.std()

        if std < 1e-6:
            std = 1e-6

        face = (face - mean) / std

        face = np.expand_dims(face, axis=0)

        return face

    except Exception as e:

        print("Preprocess Error:", e)

        return None