import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.core.config import Config

from backend.command.dispatcher import handle_command, handle_followup   # ✅ correct import

# --- (Optional) keep AI client check ---
try:
    from openai import OpenAI
    from groq import Groq
except ImportError:
    print("❌ Please install openai and groq: pip install openai groq")
    exit()

if Config.AI_PROVIDER == "groq":
    if not Config.GROQ_API_KEY or len(Config.GROQ_API_KEY) < 10:
        print("\n❌ GROQ_API_KEY missing in .env")
        exit()
    print("✅ Groq AI Provider is Active")
else:
    print("✅ OpenAI Provider is Active")

# --- Flask App ---
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

@app.route('/api/greeting', methods=['GET'])
def get_greeting():
    return jsonify({"greeting": "Hello! I am Jarvis. How may I help you?"})

# ✅ NEW: command route using dispatcher
@app.route('/api/command', methods=['POST'])
def command_route():
    data = request.json
    query = data.get('query', '').strip()
    print(f"DEBUG: query = '{query}'")

    if not query:
        return jsonify({"error": "Empty query"}), 400

    try:
        result = handle_command(query)   # calls dispatcher
        return jsonify(result)
    except Exception as e:
        print(f"🔥 ERROR: {e}")
        return jsonify({"error": str(e)}), 500

# ✅ NEW: follow‑up route
@app.route('/api/followup', methods=['POST'])
def followup_route():
    data = request.json
    action = data.get('action')
    query = data.get('query', '').strip()
    reply = handle_followup(action, query)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    print("🚀 Jarvis AI Backend is starting...")
    app.run(debug=True, port=5000)