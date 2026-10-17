import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Weather Intelligence Dashboard"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/weather")
def get_weather(city: str):

    # Step 1: Convert city name into coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}

    geo_response = httpx.get(geo_url, params=geo_params, timeout=10.0)
    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise HTTPException(status_code=404, detail="City not found")

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Fetch weather using those coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    weather_response = httpx.get(weather_url, params=weather_params, timeout=10.0)
    weather_response.raise_for_status()

    weather_data = weather_response.json()
    current_weather = weather_data["current"]

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current_weather["temperature_2m"],
        "humidity": current_weather["relative_humidity_2m"],
        "wind_speed": current_weather["wind_speed_10m"],
    }
