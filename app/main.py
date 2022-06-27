from datetime import datetime
from fastapi import FastAPI, File, UploadFile, Cookie, Response
from fastapi.responses import JSONResponse
import string
import secrets
from typing import Optional
import uuid
import uvicorn

from face_model.face_model import model
from image_operate.image_operate import img_tool_box

app = FastAPI()


def pass_gen(size=12):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    chars += "%&$#()"
    return "".join(secrets.choice(chars) for _ in range(size))


def name_gen():
    str_dt_now = time_gen()
    name = str(uuid.uuid4())[:9] + str_dt_now + ".png"
    return name


def time_gen():
    dt_now = datetime.now()
    str_dt_now = dt_now.strftime("%Y-%m-%d%H:%M:%S")
    return str_dt_now


def animal_dict_gen(animal_list):
    for index in range(len(animal_list)):
        animal_list[index] = (animal_list[index] - min(animal_list)) / (
            max(animal_list) - min(animal_list)
        )

    animal_dict = {
        "Fox": 0,
        "Rabbit": 0,
        "Wolf": 0,
        "Cat": 0,
        "Dog": 0,
        "Gorilla": 0,
        "Horse": 0,
        "Monkey": 0,
    }
    iteral = 0
    for key in animal_dict:
        animal_dict[key] += animal_list[iteral] / sum(animal_list)
        iteral += 1
    return animal_dict


@app.post("/classify")
async def return_classify_list(response: Response, file: UploadFile = File(...)):
    try:
        contents = await file.read()

        file_name = name_gen()
        cookie_pass = pass_gen()

        cv2_image = img_tool_box.contents_to_cv2(contents)
        face_image = img_tool_box.cutout_face(cv2_image)
        pil_face_image = img_tool_box.pil_to_cv2(face_image)

        predicted_animal_list = model.input_image_to_model(pil_face_image)
        predicted_animal_dict = animal_dict_gen(predicted_animal_list.tolist()[0])

        json_body = {
            "message": "Completed save img",
            "animalList": predicted_animal_dict,
        }
        response = JSONResponse(content=json_body)
        response.set_cookie(key="file_name", value=file_name)
        response.set_cookie(key="pass", value=cookie_pass)
        return response
    except Exception as e:
        print(e)
        return {"message": f"There was an error {e}"}
    finally:
        await file.close()
        img_tool_box.save_image_file(file_name, cv2_image)


@app.get("/funny_img/{animal}/")
async def return_edited_img(
    animal: str, response: Response, file_name: Optional[str] = Cookie(None)
):
    try:
        ear_attached_image = img_tool_box.attach_animal_ear(file_name, animal)
        cv2_ear_attached_image = img_tool_box.pil_to_cv2(ear_attached_image)
        anime_image = img_tool_box.anime_filter(cv2_ear_attached_image, 30)
        str_anime_image = img_tool_box.cv2_to_str(anime_image)
        response = Response(content=str_anime_image, media_type="image/png")
        return response
    except Exception as e:
        print(e)
        return {"message": f"There was an error {e}"}


if __name__ == "__main__":
    uvicorn.run(host="127.0.0.1", port=80, reload=True, log_level="info")
