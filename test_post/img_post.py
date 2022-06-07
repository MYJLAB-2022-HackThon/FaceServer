import sys
import requests

url = "http://0.0.0.0:80/api"
files = {"file": open(f"./img/test_{sys.argv[1]}.png", "rb")}
response = requests.post(url, files=files)
recv_data = response.json()
print(recv_data)
