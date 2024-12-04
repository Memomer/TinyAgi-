class AgentConfig:
    def __init__(self, role: str, api_token: str, model_id: str = "Qwen/Qwen2.5-Coder-32B-Instruct", 
                 max_tokens: int = 500, temperature: float = 0.7):
        self.role = role
        self.api_token = api_token
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.temperature = temperature
