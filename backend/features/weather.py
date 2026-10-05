from requests import get
from backend.utils.config import Config

def fetch_weather(city):
    api_key = Config.WEATHER_API_KEY
    if not api_key:
        return "Weather API key not configured."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        data = get(url).json()
        if str(data.get("cod")) == "200":
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The temperature in {city} is {temp}°C with {desc}."
        else:
            return f"City '{city}' not found."
    except Exception:
        return "Sorry, I could not fetch the weather right now."