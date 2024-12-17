from transformers import pipeline

class EmotionModel:
    def __init__(self):
        self.model = pipeline("text-classification", 
                            model="j-hartmann/emotion-english-distilroberta-base", 
                            top_k=1)

    def analyze(self, text):
        try:
            results = self.model(text)
            if results and isinstance(results, list) and len(results) > 0:
                if isinstance(results[0], dict) and 'label' in results[0]:
                    return results[0]['label']
            return "neutral"
        except Exception as e:
            print(f"Error in emotion analysis: {str(e)}")
            return "neutral"
