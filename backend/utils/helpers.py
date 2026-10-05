import datetime
import smtplib
import pyautogui
from requests import get

def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning Sir"
    elif hour < 18:
        greeting = "Good Afternoon Sir"
    else:
        greeting = "Good Evening Sir"
    return f"{greeting}. I am Jarvis Sir. Please tell me how may I help you."

def sendEmail(to, content, email_address, email_password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    server.sendmail(email_address, to, content)
    server.close()

def get_public_ip():
    return get("https://api.ipify.org").text

def take_screenshot(filename="screenshot.png"):
    img = pyautogui.screenshot()
    img.save(filename)
    return filename