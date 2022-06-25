import requests
from PIL import Image
from io import BytesIO

session = requests.Session()

url = "http://133.2.101.153:55580/classify"
files = {"file": open("./img/arimura_kasumi.png", "rb")}
response = session.post(url, files=files)
recv_data = response.json()
cookies_dict = response.cookies.get_dict()
print(cookies_dict)
print(recv_data)

url = "http://133.2.101.153:55580/funny_img/Dog"

response = session.get(url, cookies=cookies_dict)
recv_data = response.content
i = Image.open(BytesIO(recv_data))
i.save("test.png")
