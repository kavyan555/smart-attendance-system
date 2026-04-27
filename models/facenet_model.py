from facenet_pytorch import InceptionResnetV1
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def get_embedding(face_tensor):
    face_tensor = face_tensor.to(device)   # 🔥 ADD THIS
    return model(face_tensor).detach().cpu().numpy()