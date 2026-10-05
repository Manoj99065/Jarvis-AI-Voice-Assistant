# 🤖 Jarvis AI Voice Assistant

Jarvis is a Python-based AI voice assistant that listens to your voice, understands your intent, and performs tasks on your computer or the web. It combines the power of OpenAI and Groq APIs with a customizable backend and a web-based frontend.

## ✨ Features

Jarvis can handle a wide variety of tasks:

- **🗣️ Voice Interaction:** Listens to your microphone and responds with a natural voice.
- **🧠 AI Chat:** Uses OpenAI and Groq to have intelligent conversations.
- **🌐 Web Search:** Searches Wikipedia and YouTube for information and videos.
- **💻 System Control:** Opens applications (like VS Code), takes screenshots, controls volume, and runs system commands.
- **📧 Productivity:** Sends emails, writes notes, tells the time, and fetches the weather.
- **🧮 Utilities:** Calculates math problems and tells jokes.
- **🧠 Memory:** Remembers previous conversations to provide context.

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **AI Providers:** OpenAI API, Groq API
- **Frontend:** HTML, CSS, JavaScript
- **Speech Recognition:** (Uses libraries like `SpeechRecognition` and `pyttsx3` - update based on your actual requirements.txt)
- **Other APIs:** OpenWeatherMap, Gmail SMTP

## 📁 Project Structure

```text
Jarvis_Ai/
├── backend/                  # The brain of Jarvis
│   ├── command/              # Routes commands to the right skill
│   ├── core/                 # Main app loop, audio processing, intent routing
│   ├── features/             # Individual skills (weather, jokes, email, etc.)
│   ├── gui/                  # Desktop GUI animations and window
│   └── utils/                # Helper functions and memory management
├── frontend/                 # Web-based user interface
│   ├── assets/               # Images and icons
│   ├── index.html            # Main web page
│   ├── script.js             # Frontend logic
│   └── style.css             # Styling
├── .env                      # Secret API keys (Not uploaded to GitHub)
├── .gitignore                # Files to ignore in Git
├── config.py                 # Global configuration
├── main.py                   # Entry point to run Jarvis
├── requirements.txt          # Python dependencies
└── test.py                   # Test scripts





📁 Root Folder (Top Level)
These are the main files that control your project from the outside.

.env: Stores your secret API keys (OpenAI, Groq, Gmail, Weather). Remember: This is now safely hidden and won't be on GitHub.

.gitignore: Tells Git which files to ignore when uploading (like .env and __pycache__).

main.py: The starting point of your app. When you run this file, it launches Jarvis.

requirements.txt: A list of all the Python libraries your project needs. You run pip install -r requirements.txt to install them.

config.py: A global configuration file. It probably loads your API keys from .env and sets up basic settings.

test.py: A script used to test if parts of your code are working correctly.

images.jpeg & screenshot.png: Images used for your project's documentation or GUI.

📁 backend/ Folder (The Brain of Jarvis)
This is where all the logic happens. It's split into sub-folders to keep things organized.

voice_listener.py: This file is responsible for listening to your microphone. It hears what you say and converts your speech to text.

check_models.py: Checks if the AI models (like OpenAI or Groq) are available and working.

📂 backend/command/
dispatcher.py: Think of this as a "traffic cop." When you give a command, this file decides which part of the code should handle it.

📂 backend/core/
app.py: The main application loop. It ties everything together (listening, thinking, speaking).

audio.py: Handles audio processing (speech-to-text and text-to-speech).

config.py: Core configuration settings for the backend.

intent_router.py: Analyzes what you said to figure out what you want (e.g., "What's the weather?" → Intent: Weather).

route.py: Routes the identified intent to the correct feature file.

📂 backend/features/ (Jarvis's Skills)
Each file here is a specific skill Jarvis has. If you want Jarvis to do something new, you add a file here.

ai_chat.py: For general conversation with the AI.

ai_factory.py: Creates the AI connection (switching between OpenAI and Groq).

calculator.py: Does math.

email_sender.py: Sends emails using your Gmail.

groq.py: Connects to the Groq API (a fast AI service).

intent_router.py: A feature-specific intent router.

ip.py: Finds your computer's IP address.

jokes.py: Tells jokes.

memory.py: Remembers your previous conversations.

notepad.py: Writes and saves notes.

screenshot.py: Takes screenshots of your screen.

system_commands.py: Opens apps, shuts down your PC, etc.

time.py: Tells you the current time.

volume_control.py: Turns your volume up or down.

vscode.py: Opens VS Code or interacts with it.

weather.py: Gets the weather forecast.

wikipedia_search.py: Searches Wikipedia for information.

youtube.py: Plays YouTube videos.

📂 backend/gui/
animation.py: Handles animations for the desktop app.

main_window.py: Creates the main window for the desktop GUI.

📂 backend/utils/
helpers.py: Small, reusable functions used across the project.

memory.py: Helper for managing Jarvis's memory.

thread_manager.py: Runs tasks in the background so Jarvis doesn't freeze while waiting for a response.

config.py: Utility configuration.

(Note: __init__.py files are empty. They just tell Python that a folder is a package so it can be imported).

📁 frontend/ Folder (The User Interface)
This is what you see when you run the web version of Jarvis.

index.html: The main webpage structure.

script.js: The JavaScript code that makes the webpage interactive (sends commands to the backend).

style.css: Makes the webpage look nice.

assets/favicon.ico: The little icon in your browser tab.

peter.png: An image used in the web interface.

(Note: You also have __pycache__ and .pyc files in your list. These are automatically generated by Python to make your code run faster. You don't need to touch or worry about these.)

🚀 How to run your project
Open your terminal in the Jarvis_Ai folder.

Install the requirements: pip install -r requirements.txt

Run the main file: python main.py
