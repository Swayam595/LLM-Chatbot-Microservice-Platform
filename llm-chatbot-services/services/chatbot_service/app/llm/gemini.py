"""Gemini LLM Provider"""
import httpx
from app.llm.base import LLMProvider
from config import AppConfig

class GeminiLLM(LLMProvider):
    """Gemini LLM Provider"""
    llm_name = "gemini"
    
    def __init__(self):
        self.app_config = AppConfig()
        self.api_key = self.app_config.GEMINI_API_KEY
        self.endpoint = self.app_config.GEMINI_URL

    async def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM"""
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        body = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.endpoint, headers=headers, params=params, json=body)
            response.raise_for_status()
            return response
