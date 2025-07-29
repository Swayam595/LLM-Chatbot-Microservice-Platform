"""LLM Provider Factory"""
from app.llm.gemini import GeminiLLM

"""Add other providers here when needed""" #pylint: disable=pointless-string-statement
def get_llm_provider(provider: str = "gemini") -> GeminiLLM:
    """Get the LLM provider"""
    if provider == "gemini":
        return GeminiLLM()
    else:
        raise ValueError(f"Invalid provider: {provider}")
