import numpy as np

def match_face(embedding, database, threshold=0.7):
    min_dist = float('inf')
    identity = "Unknown"

    # Step 1: Find best match
    for name, db_emb in database.items():
        dist = np.linalg.norm(embedding - db_emb)

        if dist < min_dist:
            min_dist = dist
            identity = name

    # Step 2: Apply threshold
    if min_dist > threshold:
        return "Unknown"

    return identity