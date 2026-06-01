import os
import cv2
import pickle
import numpy as np

from keras_facenet import FaceNet

embedder = FaceNet()

DATASET_DIR = "dataset"

embeddings_dict = {}


# PREPROCESS FUNCTION

def preprocess_face(face):

    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

    face = cv2.resize(face, (160,160))

    face = face.astype("float32")

    return face


# GENERATE EMBEDDINGS

for person_name in os.listdir(DATASET_DIR):

    person_path = os.path.join(
        DATASET_DIR,
        person_name
    )

    if not os.path.isdir(person_path):
        continue

    person_embeddings = []

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        image = cv2.imread(image_path)

        if image is None:
            continue

        try:

            processed = preprocess_face(image)

            processed = np.expand_dims(
                processed,
                axis=0
            )

            embedding = embedder.embeddings(
                processed
            )[0]

            person_embeddings.append(
                embedding
            )

        except Exception as e:

            print(
                "Embedding Error:",
                image_name,
                e
            )

    embeddings_dict[person_name] = person_embeddings


os.makedirs(
    "embeddings",
    exist_ok=True
)

with open(
    "embeddings/embeddings.pkl",
    "wb"
) as f:

    pickle.dump(
        embeddings_dict,
        f
    )

print("\nEmbeddings Generated Successfully\n")