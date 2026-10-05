from backend.features import ai_chat, jokes, system_commands, volume_control, weather
from backend.features import wikipedia_search

class IntentRouter:
    def __init__(self, audio_engine):
        self.audio = audio_engine

    def process(self, query):
        # This method returns (response_text, should_exit)
        if "wikipedia" in query:
            return wikipedia_search.search(query), False
        elif "weather" in query:
            self.audio.speak("Tell me the city name")
            city = self.audio.listen()
            if city != "none":
                return weather.fetch_weather(city), False
            return "Could not hear city.", False
        elif "volume up" in query:
            volume_control.change_volume(0.1)
            return "Volume increased", False
        # ... add all other commands
        elif "quit" in query:
            return "Goodbye Sir!", True
        else:
            # Fallback to AI
            return ai_chat.ask_openai(query), False