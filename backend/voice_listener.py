
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.core.config import Config

# --- AI Client Setup ---
try:
    from openai import OpenAI
    from groq import Groq
except ImportError:
    print("❌ Please install required libraries: pip install openai groq")
    exit()

# Check if API Key exists in .env
if not Config.GROQ_API_KEY or len(Config.GROQ_API_KEY) < 10:
    print("\n❌ FATAL ERROR: GROQ_API_KEY is missing or invalid in your .env file!")
    print("   Please open your .env file and make sure it has:")
    print("   GROQ_API_KEY=gsk_... (your actual key)\n")
    exit()

if Config.AI_PROVIDER == "groq":
    client = Groq(api_key=Config.GROQ_API_KEY)
    print("✅ Groq AI Provider is Active")
else:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    print("✅ OpenAI Provider is Active")

# --- Flask App Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=FRONTEND_FOLDER)
CORS(app)

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

@app.route('/favicon.ico')
def favicon():
    try:
        return app.send_static_file('assets/favicon.ico')
    except:
        return '', 204

# ✅ FIXED: Added the missing /api/greeting route
@app.route('/api/greeting', methods=['GET'])
def get_greeting():
    return jsonify({
        "greeting": "Hello! I am Jarvis. How may I help you today?"
    })

@app.route('/api/command', methods=['POST'])
def handle_command():
    data = request.json
    query = data.get('query', '').strip()
    print(f"DEBUG: query = '{query}'")

    if not query:
        return jsonify({"error": "Empty query"}), 400

    try:
        # ✅ Using the most stable free Groq model
        if Config.AI_PROVIDER == "groq":
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Be short and precise."},
                    {"role": "user", "content": query}
                ],
                model="llama-3.1-8b-instant"
            )
        else:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                    {"role": "user", "content": query}
                ],
                model="gpt-3.5-turbo"
            )

        ai_reply = response.choices[0].message.content
        action, action_data = None, None

        if "open google" in query.lower():
            action, action_data = "open_url", "https://www.google.com"

        return jsonify({"reply": ai_reply, "action": action, "data": action_data})

    except Exception as e:
        print(f"🔥 ERROR from AI Provider: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Jarvis AI Backend is starting...")
    app.run(debug=True, port=5000)