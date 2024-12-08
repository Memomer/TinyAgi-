from groq import Groq
import logging

class GroqAPI:
    def __init__(self, config):
        """
        Initializes the Groq API client with the given configuration.
        :param config: Configuration object containing API key, model ID, etc.
        """
        self.client = Groq(api_key=config.api_token)  # Initialize Groq client
        self.model_id = config.model_id
        self.temperature = config.temperature

    def generate_response(self, prompt: str) -> str:
        """
        Sends a prompt to the Groq API and retrieves the generated response.
        :param prompt: The input prompt to send to the model.
        :return: The generated text response.
        """
        try:
            # Call the Groq API
            logging.info("Sending request to Groq API...")
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model_id,
                temperature=self.temperature,
            )

            # Extract the generated content
            code = response.choices[0].message.content
            logging.info("Response received successfully from Groq API.")
            return code.replace('```python', '').replace('```', '')

        except Exception as e:
            logging.error(f"Groq API call failed: {str(e)}")
            raise
