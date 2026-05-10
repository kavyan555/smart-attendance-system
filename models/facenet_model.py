from keras_facenet import FaceNet

embedder = FaceNet()


def get_embedding(face):

    if face is None:
        return None

    embeddings = embedder.embeddings(face)

    return embeddings[0]