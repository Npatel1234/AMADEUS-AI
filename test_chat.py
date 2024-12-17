import requests
import json
import time

def test_chat():
    url = "http://localhost:5000/api/chat"
    headers = {
        "Content-Type": "application/json"
    }
    
    conversation = [
        "Hello Amadeus, I'm interested in learning about quantum physics.",
        "Can you explain the double-slit experiment in simple terms?",
        "That's fascinating! How does this relate to quantum computing?",
    ]
    
    conversation_id = f"test_{int(time.time())}"
    
    for message in conversation:
        payload = {
            "message": message,
            "conversation_id": conversation_id
        }
        
        print(f"\nSending: {message}")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print("Response:", json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code}", response.text)
        
        # Small delay between messages
        time.sleep(1)
    
    # Get conversation history
    history_url = f"http://localhost:5000/api/chat/history?conversation_id={conversation_id}"
    history_response = requests.get(history_url)
    print("\nConversation History:", json.dumps(history_response.json(), indent=2))

if __name__ == "__main__":
    test_chat()