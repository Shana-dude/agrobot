import requests
from .config import OPENWEATHER_API_KEY

def get_weather(city=None, lat=None, lon=None):
    """
    Fetches real-time weather data from OpenWeatherMap by city or coordinates
    """
    if not OPENWEATHER_API_KEY:
        return "Weather API key not configured."

    if lat and lon:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    elif city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    else:
        # Fallback to a default if nothing provided
        url = f"http://api.openweathermap.org/data/2.5/weather?q=Chennai&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Weather API Error: {response.status_code}"
        
        data = response.json()
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        wind = data.get("wind", {})
        location_name = data.get("name", "Unknown Location")
        
        temp = main.get("temp", "N/A")
        desc = weather.get("description", "N/A")
        humidity = main.get("humidity", "N/A")
        wind_speed = wind.get("speed", "N/A")
        
        weather_info = f"Live Weather in {location_name}:\n"
        weather_info += f"- Temp: {temp}°C\n"
        weather_info += f"- Condition: {desc}\n"
        weather_info += f"- Humidity: {humidity}%\n"
        weather_info += f"- Wind Speed: {wind_speed} m/s\n"
        
        return weather_info

    except Exception as e:
        return f"Failed to fetch weather data: {str(e)}"
