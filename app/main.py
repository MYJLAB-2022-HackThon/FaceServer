import base64
from urllib import response
import cv2
from fastapi import FastAPI, File, UploadFile, Cookie, Response
from fastapi.responses import JSONResponse
import os
import string
import secrets
from typing import Optional
import numpy as np
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI()

UPLOAD_DIR = "/app/img/"

animal_dict = {
    "Dog": 0.21,
    "Cat": 0.01,
    "Wolf": 0.32,
    "Gorilla": 0.11,
    "Fox": 0.09,
    "Rabbit": 0.01,
    "Monkey": 0.24,
    "Horse": 0.01,
}


def transform_cv2(contents):
    base_contents = base64.b64encode(contents)
    im_bytes = base64.b64decode(base_contents)
    nparr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(nparr, flags=cv2.IMREAD_COLOR)
    return img


def save_image_file(file_name, cv2_contents):
    cv2.imwrite(os.path.join(UPLOAD_DIR + file_name), cv2_contents)


def load_image_file(file_name):
    return cv2.imread(os.path.join(UPLOAD_DIR + file_name), cv2.IMREAD_GRAYSCALE)


def transform_funny_image(img, animal):
    return img


def transform_str(cv2_img):
    _, img_arr = cv2.imencode(".png", cv2_img)
    img_enc = img_arr.tostring()
    return img_enc


def pass_gen(size=12):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chars += "%&$#()"
    return "".join(secrets.choice(chars) for _ in range(size))


@app.post("/classify")
async def return_classify_list(response: Response, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        cv2_contents = transform_cv2(contents)

        file_name = "test.png"  # いずれ乱数にする
        save_image_file(file_name, cv2_contents)
        cookie_pass = pass_gen()
        json_body = {"message": "Completed save img", "animalList": animal_dict}
        response = JSONResponse(content=json_body)
        response.set_cookie(key="file_name", value=file_name)
        response.set_cookie(key="pass", value=cookie_pass)
        return response
    except Exception as e:
        print(e)
        return {"message": f"There was an error {e}"}
    finally:
        await file.close()


@app.get("/funny_img/{animal}/")
async def return_edited_img(
    animal: str, response: Response, file_name: Optional[str] = Cookie(None)
):
    try:
        img = load_image_file(file_name)
        funny_img = transform_funny_image(img, animal)
        img_str_data = transform_str(funny_img)
        response = Response(content=img_str_data, media_type="image/png")
        return response
    except Exception as e:
        print(e)
        return {"message": f"There was an error {e}"}


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=80, reload=True, log_level="info")
