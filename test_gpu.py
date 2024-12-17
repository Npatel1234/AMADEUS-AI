import requests
import json
import time

def test_gpu_performance():
    base_url = "http://localhost:5000/api"
    
    # Check GPU status
    print("Checking GPU status...")
    response = requests.get(f"{base_url}/system/gpu")
    print(json.dumps(response.json(), indent=2))
    
    # Test chat performance
    print("\nTesting chat performance...")
    start_time = time.time()
    
    response = requests.post(
        f"{base_url}/chat",
        json={
            "message": "Write a detailed explanation of quantum entanglement in 200 words."
        }
    )
    
    end_time = time.time()
    print(f"\nResponse time: {end_time - start_time:.2f} seconds")
    print("Response:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_gpu_performance()
