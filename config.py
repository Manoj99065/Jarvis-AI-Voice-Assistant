import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")
