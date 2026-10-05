import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# .env parent directory se load karein (Jarvis_Ai)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("GROQ_API_KEY not set in .env")
else:
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
    if response.status_code == 200:
        models = response.json()
        print("Available models:")
        for model in models.get("data", []):
            print(f"  - {model['id']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")