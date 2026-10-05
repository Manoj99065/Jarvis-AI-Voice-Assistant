# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#     # Sirf 'proxies' hata do, baaki sab theek hai

#     EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
#     EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
#     WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

#     # Add these two lines inside the class
#     GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#     AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

    # Add these two lines inside the class
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "groq")