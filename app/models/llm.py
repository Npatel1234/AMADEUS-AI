import requests
import json
from config import Config

class LLMService:
    def __init__(self):
        self.config = Config()
        self.headers = {
            "Content-Type": "application/json"
        }
        
        self.system_prompt = """You are Amadeus, an advanced AI assistant inspired by Makise Kurisu from Steins;Gate. 
        Your responses should be:
        - Intelligent and scientifically accurate
        - Slightly tsundere in personality
        - Helpful while maintaining a hint of playful sarcasm
        - Knowledgeable about science, particularly physics and neuroscience
        
        Remember to stay in character while being helpful and informative."""

    def generate_response(self, user_input, max_tokens=None):
        try:
            full_prompt = f"{self.system_prompt}\n\nUser: {user_input}\nAmadeus:"
            
            payload = {
                "prompt": full_prompt,
                "max_tokens": max_tokens or self.config.MAX_TOKENS,
                "temperature": self.config.TEMPERATURE,
                "top_p": self.config.TOP_P,
                "presence_penalty": self.config.PRESENCE_PENALTY,
                "frequency_penalty": self.config.FREQUENCY_PENALTY,
                "stop": ["\nUser:", "\n\n"]
            }

            response = requests.post(
                self.config.LM_STUDIO_ENDPOINT,
                headers=self.headers,
                json=payload
            )

            if response.status_code == 200:
                return response.json()['choices'][0]['text'].strip()
            else:
                print(f"Error from LM Studio: {response.text}")
                return None

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return None
