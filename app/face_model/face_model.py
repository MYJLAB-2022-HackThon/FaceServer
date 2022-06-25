import torch
import torch.nn as nn
from torchvision import models, transforms


class face_model:
    def __init__(self) -> None:
        _device = torch.device("cpu")
        _weight = torch.load("/app/face_model.pth")
        self.load_model(_weight, _device)
        self.preprocess = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

    def load_model(self, weight, device):
        self.model_face = models.resnet18(pretrained=True)
        num_ftrs = self.model_face.fc.in_features
        self.model_face.fc = nn.Linear(num_ftrs, 8)
        self.model_face = self.model_face.to(device)
        self.model_face.load_state_dict(weight)

    def input_image_to_model(self, image_file):
        preprocess_image = self.preprocess(image_file)
        preprocess_image_batch = preprocess_image[None]
        self.model_face.eval()
        predicted_animal_list = self.model_face(preprocess_image_batch)
        return predicted_animal_list


model = face_model()
