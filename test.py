import requests
import json

url = "http://localhost:8080/calculate-cost"
headers = {"Content-Type": "application/json"}

payload = {
    "A": 1, "B": 2, "C": 1, "D": 5, "E": 1, "F": 1, "G": 2, "H": 1, "I": 1
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")