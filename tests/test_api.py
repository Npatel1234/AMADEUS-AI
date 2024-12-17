import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_chat():
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Hello Amadeus, how are you?"}
    )
    print("Chat Response:", json.dumps(response.json(), indent=2))

def test_health():
    response = requests.get("http://localhost:5000/health")
    print("Health Check:", response.json())

if __name__ == "__main__":
    test_health()
    test_chat()