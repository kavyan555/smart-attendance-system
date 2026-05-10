import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


THRESHOLD = 0.70


def match_face(embedding, database):

    best_score = -1
    identity = "Unknown"

    for person_name, embeddings in database.items():

        person_best_score = -1

        for db_embedding in embeddings:

            score = cosine_similarity(
                [embedding],
                [db_embedding]
            )[0][0]

            if score > person_best_score:
                person_best_score = score

        if person_best_score > best_score:

            best_score = person_best_score
            identity = person_name

    confidence = round(float(best_score), 2)

    if best_score < THRESHOLD:

        return "Unknown", confidence

    return identity, confidence