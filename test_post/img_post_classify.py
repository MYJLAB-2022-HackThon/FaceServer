import requests

session = requests.Session()

url = "http://133.2.101.153:55580/classify"
files = {"file": open("./img/matumoto.png", "rb")}
response = session.post(url, files=files)
recv_data = response.json()
cookies_dict = response.cookies.get_dict()
print(cookies_dict)
print(response)

# url = "http://0.0.0.0:80/img/Dog"

# response = session.get(url, cookies=cookies_dict)
# recv_data = response.json()
# print(recv_data)
# print(response)
