from backend.utils.config import Config
from backend.features.groq import ask_groq

def get_ai_response(query):
    provider = Config.AI_PROVIDER.lower()
    if provider == "groq":
        return ask_groq(query)
    elif provider == "openai":
        # TODO: implement OpenAI call
        return "OpenAI not implemented yet."
    elif provider == "gemini":
        # TODO: implement Gemini call
        return "Gemini not implemented yet."
    else:
        return "AI provider not configured. Please set AI_PROVIDER in config."