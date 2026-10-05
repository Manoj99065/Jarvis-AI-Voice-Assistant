from backend.features import ai_chat, email_sender, jokes, system_commands, volume_control, weather
from backend.features import (
    wikipedia_search
)
from backend.utils.memory import save_memory, load_memory
import datetime
import webbrowser
import os
import re



class IntentRouter:
    def __init__(self, audio_engine):
        self.audio = audio_engine

    def process(self, query):
        """
        Process the user's query and return a tuple: (response_text, should_exit)
        """
        # ---------- Core commands ----------
        if "wikipedia" in query:
            return self._handle_wikipedia(query)

        elif "weather" in query:
            return self._handle_weather()

        elif "volume up" in query:
            volume_control.change_volume(0.1)
            return "Volume increased", False
        elif "volume down" in query:
            volume_control.change_volume(-0.1)
            return "Volume decreased", False

        elif "joke" in query or "tell me a joke" in query:
            joke = jokes.get_joke()
            return joke, False

        elif "open google" in query:
            self.audio.speak("What should I search?")
            search_term = self.audio.listen()
            if search_term != "none":
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                return f"Searching Google for {search_term}", False
            else:
                return "I didn't catch that.", False

        elif "youtube" in query:
            self.audio.speak("What should I search on YouTube?")
            search_term = self.audio.listen()
            if search_term != "none":
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
                return f"Searching YouTube for {search_term}", False
            else:
                return "I didn't catch that.", False

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")
            return "Opening YouTube", False

        elif "open facebook" in query:
            webbrowser.open("https://facebook.com")
            return "Opening Facebook", False

        elif "remember that" in query:
            self.audio.speak("What should I remember?")
            data = self.audio.listen()
            if data != "none":
                save_memory(data)
                return "I will remember that.", False
            else:
                return "I didn't hear anything.", False

        elif "do you remember anything" in query:
            memory = load_memory()
            if memory:
                return f"You asked me to remember: {memory}", False
            else:
                return "I don't remember anything yet.", False

        elif "time" in query:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            return f"The time is {now}", False

        elif "ip address" in query:
            import requests
            try:
                ip = requests.get("https://api.ipify.org").text
                return f"Your IP address is {ip}", False
            except:
                return "Could not fetch IP address.", False

        elif "open notepad" in query:
            os.startfile("C:\\Windows\\notepad.exe")
            return "Opening Notepad", False

        elif "open vs code" in query:
            path = "C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
            return "Opening VS Code", False

        elif "calculate" in query:
            return self._handle_calculation(query)

        elif "screenshot" in query:
            result = system_commands.take_screenshot()
            return result, False

        elif "send email" in query:
            return self._handle_email()

        elif "set alarm" in query:
            return self._handle_alarm()

        elif "shutdown" in query:
            system_commands.shutdown()
            return "Shutting down system in 5 seconds.", True

        elif "restart" in query:
            system_commands.restart()
            return "Restarting system in 5 seconds.", True

        elif "no thanks" in query or "quit" in query or "exit" in query:
            return "Goodbye Sir! Have a nice day.", True

        else:
            # Fallback to OpenAI
            reply = ai_chat.ask_openai(query)
            return reply, False

    # ---------- Helper methods for each feature ----------
    def _handle_wikipedia(self, query):
        search = query.replace("wikipedia", "").strip()
        if not search:
            return "What do you want to search on Wikipedia?", False
        result = wikipedia_search.search(search)
        return result, False

    def _handle_weather(self):
        self.audio.speak("Tell me the city name")
        city = self.audio.listen()
        if city == "none" or not city:
            return "I could not hear the city name.", False
        result = weather.fetch_weather(city)
        return result, False

    def _handle_email(self):
        self.audio.speak("What should I say in the email?")
        content = self.audio.listen()
        if content == "none":
            return "I didn't catch the message.", False
        self.audio.speak("Whom should I send it to? (say the email address)")
        recipient = self.audio.listen()
        if recipient == "none":
            return "I didn't catch the email address.", False
        # simple validation: check if '@' in recipient
        if "@" not in recipient:
            return "That doesn't look like a valid email address.", False
        success = email_sender.send_email(recipient, content)
        if success:
            return "Email sent successfully.", False
        else:
            return "Failed to send email. Please check credentials.", False

    def _handle_calculation(self, query):
        expr = query.replace("calculate", "").strip()
        # simple safety: only allow digits, operators, parentheses, dots, spaces
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expr):
            return "I can only compute simple arithmetic expressions.", False
        try:
            result = eval(expr)
            return f"The answer is {result}", False
        except Exception:
            return "Sorry, I couldn't compute that.", False

    def _handle_alarm(self):
        self.audio.speak("Tell me the time in 24-hour format, for example 00 38 or 17 20")
        time_str = self.audio.listen()
        # Remove non‑digits and keep first 4 digits
        digits = ''.join(filter(str.isdigit, time_str))
        if len(digits) < 4:
            return "Invalid time format. Please say four digits.", False
        alarm_time = digits[:4].zfill(4)  # e.g., "0038", "1720"
        self.audio.speak(f"Alarm set for {alarm_time[:2]}:{alarm_time[2:]}")
        # Wait for alarm (with timeout after 24 hours)
        import time
        max_checks = 86400  # one second per check
        for _ in range(max_checks):
            now = datetime.datetime.now().strftime("%H%M")
            if now == alarm_time:
                self.audio.speak("Alarm ringing! Alarm ringing!")
                return "Alarm rang!", False
            time.sleep(1)
        return "Alarm time has passed.", False