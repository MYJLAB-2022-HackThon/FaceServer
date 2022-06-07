from fastapi import FastAPI, File, UploadFile
from io import BytesIO
import numpy as np
from PIL import Image
import torch
from torch import nn
import uvicorn

app = FastAPI()


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


classes = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]


def load_image_into_tensor_array(data):
    return np.array(Image.open(BytesIO(data)))


@app.post("/api")
async def img_recognize(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_image = load_image_into_tensor_array(contents)
        np_image = np.reshape(np_image, (1, 28, 28))
        tensor_image = torch.from_numpy(np_image).float()
        model = NeuralNetwork()
        model.load_state_dict(
            torch.load("./model.pth", map_location=torch.device("cpu"))
        )
        model.eval()

        with torch.no_grad():
            pred = model(tensor_image)
            predicted = classes[pred[0].argmax(0)]
            return {"Predicted": predicted}

    except Exception as e:
        print(e)
        return {"message": f"There was an error uploading {e}"}
    finally:
        await file.close()


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=80, reload=True, log_level="info")
