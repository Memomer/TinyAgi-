import requests
import logging

class HuggingFaceAPI:
    def __init__(self, config):
        self.api_url = f"https://api-inference.huggingface.co/models/{config.model_id}"
        self.headers = {
            "Authorization": f"Bearer {config.api_token}",
            "Content-Type": "application/json"
        }
        self.max_tokens = config.max_tokens
        self.temperature = config.temperature

    def generate_response(self, prompt: str) -> str:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": self.max_tokens,
                "temperature": self.temperature,
                "return_full_text": False
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            code = response.json()[0]['generated_text']
            return code.replace('```python', '').replace('```', '')
            
        except Exception as e:
            logging.error(f"API call failed: {str(e)}")
            raise
