import base64
import cv2
import dlib
from imutils import face_utils
import numpy as np
import os
from PIL import Image


ROOT_DIRECTORY = "/app/"
UP_LOAD_DIR = ROOT_DIRECTORY + "img/"


class image_operator:
    def __init__(self) -> None:
        yunet_weights = os.path.join(ROOT_DIRECTORY, "yunet.onnx")
        self.face_detector = cv2.FaceDetectorYN_create(yunet_weights, "", (0, 0))

        face_recognizer_fast_weights = os.path.join(
            ROOT_DIRECTORY, "face_recognizer_fast.onnx"
        )
        self.face_recognizer = cv2.FaceRecognizerSF_create(
            face_recognizer_fast_weights, ""
        )

        self.dlib_face_detector = dlib.get_frontal_face_detector()

        landmark_weight = os.path.join(
            ROOT_DIRECTORY, "shape_predictor_68_face_landmarks.dat"
        )
        self.landmark_predictor = dlib.shape_predictor(landmark_weight)

    # |------------------------------------------------------------------------------------
    # |Functions used by classify API
    # |------------------------------------------------------------------------------------

    def contents_to_cv2(self, contents) -> cv2:
        base_contents = base64.b64encode(contents)
        _bytes_image = base64.b64decode(base_contents)
        _np_image = np.frombuffer(_bytes_image, dtype=np.uint8)
        cv2_image = cv2.imdecode(_np_image, flags=cv2.IMREAD_COLOR)
        return cv2_image

    def cutout_face(self, cv2_image: cv2) -> cv2:
        _channels = 1 if len(cv2_image.shape) == 2 else cv2_image.shape[2]
        if _channels == 1:
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_GRAY2BGR)
        if _channels == 4:
            cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2BGR)

        _height, _width, _ = cv2_image.shape
        self.face_detector.setInputSize((_width, _height))
        _, _face_images = self.face_detector.detect(cv2_image)

        face_image = self.face_recognizer.alignCrop(cv2_image, _face_images[0])
        return face_image

    def cv2_to_pil(self, cv2_image):
        pil_image = Image.fromarray(cv2_image).convert("RGB")
        return pil_image

    async def save_image_file(self, file_name, cv2_contents):
        cv2.imwrite(os.path.join(UP_LOAD_DIR + file_name), cv2_contents)

    # |------------------------------------------------------------------------------------
    # |Functions used by funny_img API
    # |------------------------------------------------------------------------------------

    def load_image_file(self, file_name):
        gray_face_img = cv2.imread(
            os.path.join(UP_LOAD_DIR + file_name), cv2.COLOR_BGR2GRAY
        )
        return gray_face_img

    def attach_animal_ear(self, file_name, animal):
        _character_image = Image.open(os.path.join(UP_LOAD_DIR + file_name)).convert(
            "RGBA"
        )
        if animal == "Rabbit" and animal == "Horse":
            _parameter = 2
        elif animal == "Monkey":
            return _character_image
        elif animal == "Gorilla":
            gorilla_image = Image.open(
                "/app/image_operate/gorilla_img/gorilla.png"
            ).convert("RGBA")
            gorilla_image = gorilla_image.resize((_character_image.size))
            return gorilla_image
        else:
            _parameter = 1

        gray_face_image = self.load_image_file(file_name)

        faces = self.dlib_face_detector(gray_face_image, 1)

        # 顔のランドマーク検出
        landmark = self.landmark_predictor(gray_face_image, faces[0])
        # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
        landmark = face_utils.shape_to_np(landmark)

        _ear_image = Image.open(f"/app/image_operate/ear_img/{animal}.png").convert(
            "RGBA"
        )
        x, y = _ear_image.size
        scale = (landmark[16][0] - landmark[0][0]) / x
        _ear_image = _ear_image.resize((int(x * scale), int(y * scale)))

        _character_image_clear = Image.new(
            "RGBA", _character_image.size, (255, 255, 255, 0)
        )
        _character_image_clear.paste(
            _ear_image,
            (
                landmark[0][0],
                2 * landmark[28][1] - landmark[8][1] - (int(y * scale) // _parameter),
            ),
        )
        attached_image = Image.alpha_composite(_character_image, _character_image_clear)
        return attached_image

    def pil_to_cv2(self, ear_attached_image):
        np_ear_attached_image = np.array(ear_attached_image)
        cv2_ear_attached_image = cv2.cvtColor(np_ear_attached_image, cv2.COLOR_RGB2BGR)
        return cv2_ear_attached_image

    def sub_color(self, src, K):
        # 次元数を1落とす
        Z = src.reshape((-1, 3))

        # float32型に変換
        Z = np.float32(Z)

        # 基準の定義
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

        # K-means法で減色
        _, label, center = cv2.kmeans(
            Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
        )

        # UINT8に変換
        center = np.uint8(center)

        res = center[label.flatten()]

        # 配列の次元数と入力画像と同じに戻す
        return res.reshape((src.shape))

    def anime_filter(self, img, K):
        # グレースケール変換
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

        # ぼかしでノイズ低減
        edge = cv2.blur(gray, (3, 3))

        # Cannyアルゴリズムで輪郭抽出
        edge = cv2.Canny(edge, 50, 150, apertureSize=3)

        # 輪郭画像をRGB色空間に変換
        edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

        # 画像の領域分割
        img = self.sub_color(img, K)

        # 差分を返す
        return cv2.subtract(img, edge)

    def cv2_to_str(self, cv2_img):
        _, img_arr = cv2.imencode(".png", cv2_img)
        img_enc = img_arr.tostring()
        return img_enc


img_tool_box = image_operator()
