from backend.core.audio import AudioEngine

audio = AudioEngine()
audio.speak("Hello, this is a test.")
print("Listening...")
query = audio.listen()
print(f"You said: {query}")