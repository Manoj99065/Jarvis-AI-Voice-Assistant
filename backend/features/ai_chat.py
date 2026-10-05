# import openai
# from backend.core.config import OPENAI_API_KEY

# # Set API key
# openai.api_key = OPENAI_API_KEY

# def ask_openai(prompt):
#     """Get a response from OpenAI's ChatGPT."""
#     if not OPENAI_API_KEY:
#         return "OpenAI API key is missing. Please set it in .env"
#     try:
#         client = openai.OpenAI()
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=150
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"OpenAI error: {str(e)}"


import httpx
from openai import OpenAI
from backend.utils.config import Config

class JarvisAIEngine:
    def __init__(self):
        self.chat_history = [] # 👈 This is the magic. It stores the conversation.
        self.max_history = 10  # Keep only the last 10 messages to save tokens

        # Setup Groq (Primary)
        self.groq_client = OpenAI(
            api_key=Config.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            http_client=httpx.Client() # Keeps your proxy fix
        )

        # Setup OpenAI (Fallback)
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY) if Config.OPENAI_API_KEY else None

        # 👈 The upgraded System Prompt
        self.system_prompt = (
            "You are Jarvis, a highly advanced AI assistant created by Sir. "
            "You are polite, slightly witty, and always address the user as 'Sir'. "
            "You speak in English but understand Hinglish perfectly. If the user speaks Hindi, reply in Hinglish. "
            "If you don't know the answer, say: 'Sir, I don't have that information right now. Shall I search the web?' "
            "If the user asks you to do something you cannot do (like generating illegal content), politely refuse. "
            "Keep responses concise, use bullet points for lists, and be conversational."
        )

    def _get_messages(self, user_query):
        """Builds the message array with history."""
        messages = [{"role": "system", "content": self.system_prompt}]

        # Add past conversation
        messages.extend(self.chat_history)

        # Add the new question
        messages.append({"role": "user", "content": user_query})
        return messages

    def _save_to_history(self, user_query, ai_reply):
        """Saves the conversation to memory."""
        self.chat_history.append({"role": "user", "content": user_query})
        self.chat_history.append({"role": "assistant", "content": ai_reply})

        # Trim history so it doesn't get too long
        if len(self.chat_history) > self.max_history:
            self.chat_history = self.chat_history[-self.max_history:]

    def ask(self, prompt):
        """Main function to get a reply. Tries Groq first, then OpenAI."""
        messages = self._get_messages(prompt)

        # 1. TRY GROQ FIRST (Fast & Free)
        if Config.GROQ_API_KEY:
            try:
                response = self.groq_client.chat.completions.create(
                    model="openai/gpt-oss-120b", # Or "llama3-70b-8192" for better reasoning
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024 # 👈 Increased from 200. Gives proper answers.
                )
                reply = response.choices[0].message.content.strip()
                self._save_to_history(prompt, reply)
                return reply
            except Exception as e:
                print(f"⚠️ Groq failed: {e}. Falling back to OpenAI...")

        # 2. FALLBACK TO OPENAI
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo", # Or gpt-4o-mini
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                reply = response.choices[0].message.content.strip()
                self._save_to_history(prompt, reply)
                return reply
            except Exception as e:
                return f"Sir, both AI systems are currently down. Error: {str(e)}"

        return "Sir, no AI API keys are configured. Please check your .env file."

# 👇 Create a single instance to be used across your whole app
jarvis_brain = JarvisAIEngine()