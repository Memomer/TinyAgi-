class AgentConfig:
    def __init__(self, role: str, api_token: str, model_id: str = "llama3-8b-8192", 
                 max_tokens: int = 500, temperature: float = 0.7):
        """
        Configuration for the agent and API interactions.
        :param role: Role or description of the agent.
        :param api_token: API token for authentication (e.g., Groq API key).
        :param model_id: Model ID to be used (default is Groq's Llama model).
        :param max_tokens: Maximum number of tokens for responses.
        :param temperature: Sampling temperature for the LLM.
        """
        self.role = role
        self.api_token = api_token
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
