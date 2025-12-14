"""
Client for interacting with LLM (LM Studio/GigaChat).
"""
from openai import OpenAI
from src.core.config import config

class LLMClient:
    """Client for LLM API."""
    
    def __init__(self):
        self.client = OpenAI(
            base_url=config.LM_STUDIO_BASE_URL,
            api_key=config.LM_STUDIO_API_KEY
        )
    
    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate text from prompt."""
        try:
            completion = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"LLM connection error: {e}")
    
    def generate_sql(self, question: str, schema: str) -> str:
        """Generate SQL query from question."""
        # This will be implemented with proper prompts
        pass
