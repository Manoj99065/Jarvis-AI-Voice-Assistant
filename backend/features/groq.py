# # # =from openai import OpenAI
# # from backend.utils.config import Config

# # client = OpenAI(
# #     api_key=Config.GROQ_API_KEY,
# #     base_url="https://api.groq.com/openai/v1"
# # )

# # def ask_groq(prompt):
# #     if not Config.GROQ_API_KEY:
# #         return "Groq API key missing. Set GROQ_API_KEY in .env"

# #     try:
# #         response = client.chat.completions.create(
# #             model="openai/gpt-oss-120b",   # Choose one from the list
# #             messages=[
# #                 {
# #                     "role": "system",
# #                     "content": (
# #                         "You are Jarvis, a friendly and witty AI assistant. "
# #                         "You speak in a mix of English and Hindi (Hinglish) if the user uses Hindi. "
# #                         "Keep responses short, helpful, and conversational. "
# #                         "Always address the user as 'Sir' or 'Madam'."
# #                     )
# #                 },
# #                 {"role": "user", "content": prompt}
# #             ],
# #             temperature=0.8,
# #             max_tokens=200
# #         )
# #         return response.choices[0].message.content.strip()
# #     except Exception as e:
# #         return f"Groq error: {str(e)}"

# from openai import OpenAI
# from backend.utils.config import Config

# # 1. Setup the Groq client using the OpenAI-compatible API
# client = OpenAI(
#     api_key=Config.GROQ_API_KEY,
#     base_url="https://api.groq.com/openai/v1"
# )

# # 2. The main function that Jarvis will call
# def ask_groq(prompt):
#     # Check if the API key is actually set
#     if not Config.GROQ_API_KEY:
#         return "Groq API key missing. Set GROQ_API_KEY in .env"

#     try:
#         # 3. Send the request to Groq
#         response = client.chat.completions.create(
#             # Use a model that is currently active.
#             # You can also use "openai/gpt-oss-120b" or "qwen/qwen3.6-27b".
#             model="openai/gpt-oss-120b",
#             messages=[
#                 # 4. System prompt: This defines Jarvis's personality
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are Jarvis, a friendly and witty AI assistant. "
#                         "You speak in a mix of English and Hindi (Hinglish) if the user uses Hindi. "
#                         "Keep responses short, helpful, and conversational. "
#                         "Always address the user as 'Sir' or 'Madam'."
#                     )
#                 },
#                 # 5. The user's actual query
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.8,      # Controls creativity (0.0 = strict, 1.0 = creative)
#             max_tokens=200        # Maximum length of the reply
#         )
#         # 6. Return the reply
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         # 7. If something fails, return the error message (so it doesn't crash the server)
#         return f"Groq error: {str(e)}"

from openai import OpenAI
from backend.utils.config import Config
import httpx   # <-- Add this import

# 1. Setup the Groq client using the OpenAI-compatible API
#    Use a custom http_client to avoid the internal proxy error.
http_client = httpx.Client()   # No proxy by default – add proxy string here if needed

client = OpenAI(
    api_key=Config.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    http_client=http_client   # <-- This bypasses the problematic internal client creation
)

# 2. The main function that Jarvis will call
def ask_groq(prompt):
    # Check if the API key is actually set
    if not Config.GROQ_API_KEY:
        return "Groq API key missing. Set GROQ_API_KEY in .env"

    try:
        # 3. Send the request to Groq
        response = client.chat.completions.create(
            # Use a model that is currently active.
            # You can also use "openai/gpt-oss-120b" or "qwen/qwen3.6-27b".
            model="openai/gpt-oss-120b",
            messages=[
                # 4. System prompt: This defines Jarvis's personality
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a friendly and witty AI assistant. "
                        "You speak in a mix of English and Hindi (Hinglish) if the user uses Hindi. "
                        "Keep responses short, helpful, and conversational. "
                        "Always address the user as 'Sir' or 'Madam'."
                    )
                },
                # 5. The user's actual query
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,      # Controls creativity (0.0 = strict, 1.0 = creative)
            max_tokens=200        # Maximum length of the reply
        )
        # 6. Return the reply
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 7. If something fails, return the error message (so it doesn't crash the server)
        return f"Groq error: {str(e)}"