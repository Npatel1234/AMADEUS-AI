from datetime import datetime
import json

class ConversationManager:
    def __init__(self):
        self.max_history_size = 5
        self.conversations = {}
        self.prompt_templates = {
            'chat': """
            You are Amadeus, an advanced AI assistant inspired by Makise Kurisu from Steins;Gate.
            Your personality traits:
            - Intelligent and scientifically accurate
            - Slightly tsundere in personality
            - Helpful while maintaining a hint of playful sarcasm
            - Knowledgeable about science, particularly physics and neuroscience
            
            Important: Always give unique responses and avoid repeating yourself.
            Stay in character but be dynamic in your conversations.
            """,
            'code': """
            You are Amadeus, an advanced AI coding assistant. 
            When analyzing code or solving programming problems:
            - Provide clear, detailed explanations
            - Include code examples when relevant
            - Break down complex problems into steps
            - Suggest best practices and optimizations
            - If there are multiple solutions, explain the trade-offs
            
            Format your responses in markdown for better readability.
            """,
            'summary': """
            You are Amadeus, an advanced AI assistant for text analysis.
            When summarizing text:
            - Provide a concise overview of the main points
            - Highlight key concepts and ideas
            - Maintain the original meaning and context
            - Structure the summary in a clear, organized manner
            - Include important details while omitting unnecessary information
            """
        }

    def add_exchange(self, conversation_id, user_message, ai_response):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Check if this would be a repetitive response
        recent_responses = [ex['ai_response'] for ex in self.conversations[conversation_id][-3:]]
        if ai_response in recent_responses:
            # Generate a marker for the LLM to try again
            return False
        
        exchange = {
            'user_message': user_message,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat()
        }
        
        self.conversations[conversation_id].append(exchange)
        
        if len(self.conversations[conversation_id]) > self.max_history_size:
            self.conversations[conversation_id].pop(0)
        
        return True

    def generate_contextual_prompt(self, conversation_id, current_message, prompt_type='chat'):
        context = [self.prompt_templates.get(prompt_type, self.personality_prompt)]
        
        if conversation_id in self.conversations:
            history = self.conversations[conversation_id][-3:]
            unique_responses = set()
            
            for exchange in history:
                if exchange['ai_response'] not in unique_responses:
                    context.append(f"User: {exchange['user_message']}")
                    context.append(f"Amadeus: {exchange['ai_response']}\n")
                    unique_responses.add(exchange['ai_response'])
        
        context.append(f"Current user message: {current_message}")
        context.append("Respond as Amadeus:")
        
        return "\n".join(context)

    def extract_main_topic(self, conversation_id):
        if conversation_id in self.conversations and self.conversations[conversation_id]:
            last_exchange = self.conversations[conversation_id][-1]
            return f"{last_exchange['user_message'][:50]}..."
        return "various topics"

    def save_conversations(self):
        with open('conversations.json', 'w') as f:
            json.dump(self.conversations, f)

    def load_conversations(self):
        try:
            with open('conversations.json', 'r') as f:
                self.conversations = json.load(f)
        except FileNotFoundError:
            self.conversations = {}

    def get_conversation_history(self, conversation_id):
        return self.conversations.get(conversation_id, [])

    def clear_conversation(self, conversation_id):
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            self.save_conversations()