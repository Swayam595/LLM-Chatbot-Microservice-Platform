"""LLM Provider Base Class"""
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """LLM Provider"""
    llm_name: str

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM"""