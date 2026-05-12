import requests

def get_weather(city: str) -> str:
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        data = response.json()

        current = data["current_condition"][0]
        area = data["nearest_area"][0]

        city_name = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        temp_c = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        weather_desc = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        visibility = current["visibility"]

        return (
            f"🌤️ Weather in {city_name}, {country}:\n"
            f"   🌡️ Temperature: {temp_c}°C (Feels like {feels_like}°C)\n"
            f"   ☁️ Condition: {weather_desc}\n"
            f"   💧 Humidity: {humidity}%\n"
            f"   💨 Wind Speed: {wind_speed} km/h\n"
            f"   👁️ Visibility: {visibility} km\n"
        )

    except Exception as e:
        return f"Weather fetch error: {str(e)}"


WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather information for any city in the world.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name e.g. Ranchi, Mumbai, London, New York"
                }
            },
            "required": ["city"]
        }
    }
}