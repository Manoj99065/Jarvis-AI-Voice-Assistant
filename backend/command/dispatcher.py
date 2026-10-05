import datetime
import webbrowser
import os
import threading
import re
from backend.features import (
    wikipedia_search,
    weather,
    youtube,
    jokes,
    time as time_module,
    ip,
    calculator,
    screenshot,
    email_sender,
    system_commands,
    volume_control,
    memory,
    notepad,
    vscode,
)
from backend.utils.helpers import wishMe


# ============================================================
#  HELPER
# ============================================================
def contains_any(query, phrases):
    """Return True if query contains any phrase as a WHOLE WORD."""
    query_lower = query.lower()
    for phrase in phrases:
        pattern = r'\b' + re.escape(phrase.lower()) + r'\b'
        if re.search(pattern, query_lower):
            return True
    return False


# ============================================================
#  PHRASE LISTS
# ============================================================

GREETING_PHRASES = [
    "hello", "hi", "hey", "hii", "hye", "namaste", "नमस्ते",
    "kese ho", "kaise ho", "how are you", "how r u",
    "good morning", "good afternoon", "good evening", "good night"
]

WIKIPEDIA_PHRASES = ["wikipedia", "विकिपीडिया"]
WIKIPEDIA_OPEN_PHRASES = [
    "open wikipedia", "wikipedia kholo", "विकिपीडिया खोलो",
    "wikipedia open", "विकिपीडिया चालू करो"
]

YOUTUBE_PHRASES = [
    "open youtube", "youtube kholo", "यूट्यूब खोलो",
    "youtube open", "open utube"
]
FACEBOOK_PHRASES = [
    "open facebook", "facebook kholo", "फेसबुक खोलो",
    "fb kholo", "open fb"
]
INSTAGRAM_PHRASES = [
    "open instagram", "instagram kholo", "इंस्टाग्राम खोलो",
    "insta kholo", "open insta"
]
WHATSAPP_PHRASES = [
    "open whatsapp", "whatsapp kholo", "व्हाट्सएप खोलो",
    "wa kholo", "open wa"
]
TWITTER_PHRASES = [
    "open twitter", "twitter kholo", "open x", "x kholo",
    "ट्विटर खोलो", "twitter open"
]
LINKEDIN_PHRASES = [
    "open linkedin", "linkedin kholo", "लिंक्डइन खोलो",
    "linkedin open"
]
GITHUB_PHRASES = [
    "open github", "github kholo", "गिटहब खोलो",
    "github open"
]

GOOGLE_SEARCH_PHRASES = [
    "open google", "search google", "google kholo",
    "गूगल खोलो", "गूगल सर्च", "google search"
]

FILE_EXPLORER_PHRASES = [
    "open file explorer", "open files", "file explorer kholo",
    "फाइल एक्सप्लोरर खोलो", "explorer open"
]

WEATHER_PHRASES = [
    "weather", "mausam", "mosam", "मौसम", "weather forecast",
    "temperature", "temp", "degree", "garmi", "sardi", "barish",
    "तापमान"
]

ALARM_PHRASES = [
    "set alarm", "alarm set", "alarm lagao", "अलार्म सेट करो",
    "अलार्म लगाओ", "alarm banao", "alarm rakh do"
]

VOLUME_UP_PHRASES = [
    "volume up", "voujum bdao", "avaj bdao", "sound up",
    "sound increase", "volume increase",
    "वॉल्यूम बढ़ाओ", "आवाज बढ़ाओ", "volume badhao",
    "volume high", "sound high", "tez karo"
]
VOLUME_DOWN_PHRASES = [
    "volume down", "voujum kam", "avaj kam", "sound down",
    "sound decrease", "volume decrease",
    "वॉल्यूम कम करो", "आवाज कम करो", "volume kam karo",
    "volume low", "sound low", "dheere karo"
]

JOKE_PHRASES = [
    "joke", "mazaak", "चुटकुला", "tell me a joke",
    "joke sunao", "mazaak sunao", "hasao"
]

YOUTUBE_SEARCH_PHRASES = [
    "youtube search", "search youtube", "play youtube",
    "youtube par search karo", "यूट्यूब सर्च",
    "youtube par chalao", "youtube pe search"
]

REMEMBER_PHRASES = [
    "remember that", "yaad rakho", "याद रखो",
    "remember this", "yaad karo"
]
REMEMBER_QUERY_PHRASES = [
    "do you remember anything", "kya yaad hai", "क्या याद है",
    "what do you remember", "tell me what you remember"
]

TIME_PHRASES = [
    "time", "samay", "kya time hai", "क्या समय है",
    "time batao", "samay batao", "current time",
    "abhi kya time hua", "waqt kya hai"
]

IP_PHRASES = [
    "ip address", "ip pata", "आईपी एड्रेस",
    "ip batao", "my ip", "mera ip"
]

NOTEPAD_PHRASES = [
    "open notepad", "notepad kholo", "नोटपैड खोलो",
    "notepad open"
]
VSCODE_PHRASES = [
    "open vs code", "vs code kholo", "वीएस कोड खोलो",
    "visual studio code", "vscode open"
]

CALCULATE_PHRASES = [
    "calculate", "compute", "solve", "गणना करो",
    "kya hoga", "what is"
]

SCREENSHOT_PHRASES = [
    "screenshot", "screen capture", "screenshot lo",
    "स्क्रीनशॉट लो", "screen shot", "capture screen"
]

EMAIL_PHRASES = [
    "send email", "email bhejo", "ईमेल भेजो",
    "mail bhejo", "send mail"
]

SHUTDOWN_PHRASES = [
    "shutdown", "system band karo", "सिस्टम बंद करो",
    "shut down", "band kar"
]
RESTART_PHRASES = [
    "restart", "system restart karo", "सिस्टम रीस्टार्ट करो",
    "reboot", "reload"
]
LOCK_PHRASES = [
    "lock screen", "screen lock karo", "स्क्रीन लॉक करो",
    "lock computer", "pc lock"
]
SLEEP_PHRASES = [
    "sleep system", "system sleep karo", "सिस्टम स्लीप करो",
    "sleep mode", "suspend"
]

QUIT_PHRASES = [
    "quit", "exit", "bye", "no thanks", "alvida", "बाय",
    "goodbye", "see you", "bye bye", "tata"
]

# ============================================================
#  SYSTEM COMMAND PHRASES (NEW - YEH MISSING THE!)
# ============================================================
HIBERNATE_PHRASES = [
    "hibernate", "hibernate karo", "system hibernate",
    "hibernate mode"
]
CANCEL_SHUTDOWN_PHRASES = [
    "cancel shutdown", "shutdown cancel karo",
    "abort shutdown", "shutdown rok do"
]
BATTERY_PHRASES = [
    "battery", "charge", "battery kitni hai",
    "battery status", "battery percentage"
]
CPU_PHRASES = [
    "cpu", "processor", "cpu usage",
    "cpu kitna", "cpu check karo"
]
RAM_PHRASES = [
    "ram", "memory usage", "ram kitni hai",
    "memory kitni", "ram check karo"
]
DISK_PHRASES = [
    "disk", "storage", "disk usage",
    "hard disk", "disk check karo"
]
SYSTEM_INFO_PHRASES = [
    "system info", "system information", "pc info",
    "computer info", "mera system info"
]
WIFI_PASSWORD_PHRASES = [
    "wifi password", "wifi ka password",
    "wifi password batao", "wifi password nikal"
]
INTERNET_CHECK_PHRASES = [
    "internet check", "internet hai",
    "internet working", "net check karo"
]
RECYCLE_BIN_PHRASES = [
    "empty recycle bin", "recycle bin khali karo",
    "trash clear karo", "recycle bin saaf karo"
]
BRIGHTNESS_UP_PHRASES = [
    "brightness badhao", "brightness up",
    "screen bright karo", "brightness increase"
]
BRIGHTNESS_DOWN_PHRASES = [
    "brightness kam karo", "brightness down",
    "screen dim karo", "brightness decrease"
]
PROCESS_PHRASES = [
    "process list", "running processes",
    "kya chal raha hai", "processes"
]
OPEN_CMD_PHRASES = [
    "open cmd", "cmd kholo",
    "open terminal", "terminal kholo"
]
CLOSE_APP_PHRASES = [
    "close app", "close chrome", "close notepad",
    "band karo", "close application"
]


# ============================================================
#  MAIN HANDLER
# ============================================================
def handle_command(query):
    try:
        print(f"DEBUG: query = '{query}'")
        response = {"reply": "", "action": None, "data": None}

        # ---- Wikipedia ----
        if contains_any(query, WIKIPEDIA_OPEN_PHRASES):
            response["reply"] = "Opening Wikipedia"
            response["action"] = "open_url"
            response["data"] = "https://wikipedia.org"
        elif contains_any(query, WIKIPEDIA_PHRASES):
            response["reply"] = wikipedia_search.search_wikipedia(query)

        # ---- Websites ----
        elif contains_any(query, YOUTUBE_PHRASES):
            response["reply"] = youtube.open_youtube()
            response["action"] = "open_url"
            response["data"] = "https://youtube.com"
        # elif contains_any(query, YOUTUBE_PHRASES):
        #     response["reply"] = youtube.open_youtube()
        #     response["action"] = "open_url"
        #     response["data"] = "https://youtube.com"

        elif contains_any(query, FACEBOOK_PHRASES):
            response["reply"] = "Opening Facebook"
            response["action"] = "open_url"
            response["data"] = "https://facebook.com"

        elif contains_any(query, INSTAGRAM_PHRASES):
            response["reply"] = "Opening Instagram"
            response["action"] = "open_url"
            response["data"] = "https://instagram.com"

        elif contains_any(query, WHATSAPP_PHRASES):
            response["reply"] = "Opening WhatsApp Web"
            response["action"] = "open_url"
            response["data"] = "https://web.whatsapp.com"

        elif contains_any(query, TWITTER_PHRASES):
            response["reply"] = "Opening Twitter (X)"
            response["action"] = "open_url"
            response["data"] = "https://twitter.com"

        elif contains_any(query, LINKEDIN_PHRASES):
            response["reply"] = "Opening LinkedIn"
            response["action"] = "open_url"
            response["data"] = "https://linkedin.com"

        elif contains_any(query, GITHUB_PHRASES):
            response["reply"] = "Opening GitHub"
            response["action"] = "open_url"
            response["data"] = "https://github.com"

        # ---- Google Search ----
        elif contains_any(query, GOOGLE_SEARCH_PHRASES):
            response["reply"] = "What should I search on Google?"
            response["action"] = "ask_followup"
            response["data"] = "google_search"

        # ---- File Explorer ----
        elif contains_any(query, FILE_EXPLORER_PHRASES):
            response["reply"] = "Opening File Explorer"
            os.startfile("C:\\")

        # ---- Weather ----
        elif contains_any(query, WEATHER_PHRASES):
            response["reply"] = "Please tell me the city name."
            response["action"] = "ask_followup"
            response["data"] = "weather"

        # ---- Alarm ----
        elif contains_any(query, ALARM_PHRASES):
            response["reply"] = "Please tell me the time in 24-hour format, like 14 30."
            response["action"] = "ask_followup"
            response["data"] = "alarm"

        # ---- Volume ----
        elif contains_any(query, VOLUME_UP_PHRASES):
            try:
                new_vol = volume_control.change_volume(0.1)
                response["reply"] = f"Volume increased to {int(new_vol*100)}%" if new_vol is not None else "Volume increased (approximate)."
            except Exception as e:
                response["reply"] = f"Sorry, I couldn't increase volume: {str(e)}"

        elif contains_any(query, VOLUME_DOWN_PHRASES):
            try:
                new_vol = volume_control.change_volume(-0.1)
                response["reply"] = f"Volume decreased to {int(new_vol*100)}%" if new_vol is not None else "Volume decreased (approximate)."
            except Exception as e:
                response["reply"] = f"Sorry, I couldn't decrease volume: {str(e)}"

        # ---- Joke ----
        elif contains_any(query, JOKE_PHRASES):
            response["reply"] = jokes.get_joke()

        # ---- YouTube search ----
        elif contains_any(query, YOUTUBE_SEARCH_PHRASES):
            response["reply"] = "What should I search on YouTube?"
            response["action"] = "ask_followup"
            response["data"] = "youtube_search"

        # ---- Memory ----
        elif contains_any(query, REMEMBER_PHRASES):
            response["reply"] = "What should I remember?"
            response["action"] = "ask_followup"
            response["data"] = "remember"

        elif contains_any(query, REMEMBER_QUERY_PHRASES):
            mem = memory.load_memory()
            response["reply"] = f"You asked me to remember: {mem}" if mem else "I don't remember anything yet."

        # ---- Time ----
        elif contains_any(query, TIME_PHRASES):
            now = datetime.datetime.now().strftime("%I:%M %p")
            response["reply"] = f"The current time is {now}"

        # ---- IP ----
        elif contains_any(query, IP_PHRASES):
            response["reply"] = ip.get_ip()

        # ---- Open Notepad ----
        elif contains_any(query, NOTEPAD_PHRASES):
            response["reply"] = notepad.open_notepad()

        # ---- Open VS Code ----
        elif contains_any(query, VSCODE_PHRASES):
            response["reply"] = vscode.open_vscode()

        # ---- Calculate ----
        elif contains_any(query, CALCULATE_PHRASES):
            expression = query
            for word in CALCULATE_PHRASES:
                expression = expression.replace(word, "").strip()
            response["reply"] = calculator.calculate(expression)

        # ---- Screenshot ----
        elif contains_any(query, SCREENSHOT_PHRASES):
            response["reply"] = screenshot.capture_screenshot()

        # ---- Email ----
        elif contains_any(query, EMAIL_PHRASES):
            response["reply"] = "What should I say in the email?"
            response["action"] = "ask_followup"
            response["data"] = "email"

        # ---- System: Power ----
        elif contains_any(query, SHUTDOWN_PHRASES):
            response["reply"] = system_commands.shutdown()
            response["action"] = "shutdown"

        elif contains_any(query, RESTART_PHRASES):
            response["reply"] = system_commands.restart()
            response["action"] = "restart"

        elif contains_any(query, LOCK_PHRASES):
            response["reply"] = system_commands.lock_screen()

        elif contains_any(query, SLEEP_PHRASES):
            response["reply"] = system_commands.sleep_system()

        elif contains_any(query, HIBERNATE_PHRASES):
            response["reply"] = system_commands.hibernate()

        elif contains_any(query, CANCEL_SHUTDOWN_PHRASES):
            response["reply"] = system_commands.cancel_shutdown()

        # ---- System: Info ----
        elif contains_any(query, BATTERY_PHRASES):
            response["reply"] = system_commands.get_battery()

        elif contains_any(query, CPU_PHRASES):
            response["reply"] = system_commands.get_cpu_usage()

        elif contains_any(query, RAM_PHRASES):
            response["reply"] = system_commands.get_ram_usage()

        elif contains_any(query, DISK_PHRASES):
            response["reply"] = system_commands.get_disk_usage()

        elif contains_any(query, SYSTEM_INFO_PHRASES):
            response["reply"] = system_commands.get_system_info()

        # ---- System: Network ----
        elif contains_any(query, WIFI_PASSWORD_PHRASES):
            response["reply"] = system_commands.get_wifi_password()

        elif contains_any(query, INTERNET_CHECK_PHRASES):
            response["reply"] = system_commands.check_internet()

        # ---- System: Misc ----
        elif contains_any(query, RECYCLE_BIN_PHRASES):
            response["reply"] = system_commands.empty_recycle_bin()

        elif contains_any(query, BRIGHTNESS_UP_PHRASES):
            response["reply"] = system_commands.set_brightness(90)

        elif contains_any(query, BRIGHTNESS_DOWN_PHRASES):
            response["reply"] = system_commands.set_brightness(30)

        elif contains_any(query, PROCESS_PHRASES):
            response["reply"] = system_commands.list_processes()

        elif contains_any(query, OPEN_CMD_PHRASES):
            response["reply"] = system_commands.open_cmd()

        elif contains_any(query, CLOSE_APP_PHRASES):
            app_name = query.replace("close", "").replace("band karo", "").strip()
            response["reply"] = system_commands.close_app(app_name) if app_name else "Which app should I close, Sir?"

        # ---- Quit ----
        elif contains_any(query, QUIT_PHRASES):
            response["reply"] = "Thanks for using me Sir. Have a good day."
            response["action"] = "quit"

        # ---- GREETING (near bottom) ----
        elif contains_any(query, GREETING_PHRASES):
            response["reply"] = "Namaste Sir! Main theek hoon. Aap kaise ho?"

        # ---- FALLBACK: AI ----
        else:
            from backend.features.ai_chat import jarvis_brain
            response["reply"] = jarvis_brain.ask(query)

        return response

    except Exception as e:
        return {"reply": f"Error: {str(e)}", "action": None, "data": None}


# ============================================================
#  FOLLOW-UP HANDLER
# ============================================================
def handle_followup(action, data, query):
    if action == "weather":
        return weather.fetch_weather(query)
    elif action == "youtube_search":
        return youtube.search_youtube(query)
    elif action == "google_search":
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for '{query}'"
    elif action == "remember":
        memory.save_memory(query)
        return "I will remember that."
    elif action == "email":
        return "Please tell me the recipient's email address."
    elif action == "alarm":
        def alarm_worker(time_str):
            import time
            while True:
                now = datetime.datetime.now().strftime("%H%M")
                if now == time_str:
                    print("ALARM!")
                    break
                time.sleep(1)
        threading.Thread(target=alarm_worker, args=(query,), daemon=True).start()
        return f"Alarm set for {query[:2]}:{query[2:]}"
    else:
        return "I didn't understand the follow-up."