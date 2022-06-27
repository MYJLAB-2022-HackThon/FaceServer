import requests

url = "http://0.0.0.0:80/img/Dog"

cookies_dict = {"set-cookie": "test.png"}
response = requests.get(url, cookies=cookies_dict)
recv_data = response.json()
print(recv_data)
print(response)
