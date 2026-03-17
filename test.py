import requests

url = "http://127.0.0.1:5000/api/corregir"
data = {
    "texto": "estoo es un textoo de pueva. espero q funsione",
    "nivel_correccion": "ortografia"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
