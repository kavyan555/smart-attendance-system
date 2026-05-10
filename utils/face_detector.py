from mtcnn import MTCNN
import cv2

detector = MTCNN()


def detect_faces(image):

    rgb_image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    results = detector.detect_faces(rgb_image)

    faces = []

    h, w, _ = image.shape

    for result in results:

        x, y, width, height = result['box']

        if width <= 0 or height <= 0:
            continue

        x1 = max(0, x)
        y1 = max(0, y)

        x2 = min(w, x + width)
        y2 = min(h, y + height)

        if (x2 - x1) < 50 or (y2 - y1) < 50:
            continue

        if x2 <= x1 or y2 <= y1:
            continue

        faces.append((x1, y1, x2, y2))

    return faces