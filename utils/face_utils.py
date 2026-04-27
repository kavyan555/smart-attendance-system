import cv2
import torch

def preprocess_face(face):
    face = cv2.resize(face, (160, 160))
    face = face / 255.0
    face = face.transpose(2, 0, 1)
    
    face = torch.tensor(face, dtype=torch.float32)  # 🔥 convert to tensor
    face = face.unsqueeze(0)  # add batch dimension

    return face