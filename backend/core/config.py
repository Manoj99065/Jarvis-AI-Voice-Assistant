# # # # import os
# # # # from dotenv import load_dotenv

# # # # load_dotenv()  # loads .env from project root

# # # # class Config:
# # # #     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# # # #     EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
# # # #     EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# # # #     WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# # import os
# # import json
# # from flask import Flask, request, jsonify, send_from_directory
# # from flask_cors import CORS
# # from backend.utils.config import Config  # ✅ Correct import





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