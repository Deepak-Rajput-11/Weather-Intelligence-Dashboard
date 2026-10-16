import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to Weather Intelligence Dashboard"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/weather")
def get_weather():
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 28.61,
        "longitude": 77.21,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    }

    response = httpx.get(url, params=params, timeout=10.0)
    response.raise_for_status()

    data = response.json()
    current_weather = data["current"]

    return {
        "city": "Delhi",
        "temperature": current_weather["temperature_2m"],
        "humidity": current_weather["relative_humidity_2m"],
        "wind_speed": current_weather["wind_speed_10m"],
    }
