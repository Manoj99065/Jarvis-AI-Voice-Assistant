# import pyttsx3
# import speech_recognition as sr

# class AudioEngine:
#     def __init__(self):
#         self.engine = pyttsx3.init('sapi5')
#         voices = self.engine.getProperty('voices')
#         self.engine.setProperty('voice', voices[1].id)
#         self.engine.setProperty('rate', 220)
#         self.recognizer = sr.Recognizer()

#     def speak(self, text):
#         self.engine.say(text)
#         self.engine.runAndWait()

#     def listen(self):
#         with sr.Microphone() as source:
#             self.recognizer.pause_threshold = 1
#             audio = self.recognizer.listen(source)
#         try:
#             query = self.recognizer.recognize_google(audio, language='en-in')
#             return query.lower()
#         except:
#             return "none"


import pyttsx3
import speech_recognition as sr

class AudioEngine:
    def __init__(self):
        print("🚨 ENGINE CREATED") # <-- ADD THIS
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 220)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        print(f"🗣️ SPEAK CALLED: {text}") # <-- ADD THIS
        self.engine.stop() # <-- ADD THIS (Clears old queue)
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop() # <-- ADD THIS (Clears queue after speaking)

    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)
        try:
            query = self.recognizer.recognize_google(audio, language='en-in')
            return query.lower()
        except:
            return "none"