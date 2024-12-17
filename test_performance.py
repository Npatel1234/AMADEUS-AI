import requests
import json
import time
import psutil

def monitor_resources():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    return {
        'cpu': cpu_percent,
        'memory': memory.percent
    }

def test_chat_performance():
    base_url = "http://localhost:5000/api"
    
    # Test messages of increasing complexity
    messages = [
        "Hello!",  # Simple
        "What is quantum physics?",  # Medium
        "Explain the relationship between quantum mechanics and consciousness in detail.",  # Complex
    ]
    
    for message in messages:
        print(f"\nTesting with message: {message}")
        print("System resources before request:")
        print(json.dumps(monitor_resources(), indent=2))
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/chat",
            json={"message": message}
        )
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print("System resources after request:")
        print(json.dumps(monitor_resources(), indent=2))
        print("\nResponse:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_chat_performance()