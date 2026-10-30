import httpx
import time
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_weather_description(code: int) -> str:
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_codes.get(code, "Unknown weather condition")


def fetch_api_data(url: str, params: dict) -> dict:
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = httpx.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError:
            if attempt == max_attempts - 1:
                raise HTTPException(
                    status_code=503,
                    detail="Weather service is temporarily unavailable",
                )

        except httpx.HTTPStatusError as error:
            if error.response.status_code < 500:
                raise HTTPException(
                    status_code=502,
                    detail="External weather API returned an error",
                )

            if attempt == max_attempts - 1:
                raise HTTPException(
                    status_code=502,
                    detail="External weather API returned an error",
                )

        if attempt < max_attempts - 1:
            time.sleep(1)


def get_city_location(city: str) -> dict:
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    geo_data = fetch_api_data(geo_url, geo_params)

    if not geo_data.get("results"):
        raise HTTPException(status_code=404, detail="City not found")

    return geo_data["results"][0]


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/weather")
def get_weather(
    city: str = Query(
        min_length=2, max_length=100, pattern=r".*\S.*", strip_whitespace=True
    )
) -> dict:

    # Step 1: Find the city
    location = get_city_location(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Fetch weather using those coordinates
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    }

    weather_data = fetch_api_data(weather_url, weather_params)

    current_weather = weather_data.get("current")
    if not current_weather:
        raise HTTPException(
            status_code=502,
            detail="Weather service returned incomplete current weather data",
        )

    required_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "weather_code",
    ]

    if not all(field in current_weather for field in required_fields):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned incomplete current weather data",
        )

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current_weather["temperature_2m"],
        "humidity": current_weather["relative_humidity_2m"],
        "wind_speed": current_weather["wind_speed_10m"],
        "weather_code": current_weather["weather_code"],
        "weather_description": get_weather_description(current_weather["weather_code"]),
    }


@app.get("/forecast")
@app.get("/forecast")
def get_forecast(
    city: str = Query(
        min_length=2, max_length=100, pattern=r".*\S.*", strip_whitespace=True
    )
) -> dict:
    # Step 1: Find the city
    location = get_city_location(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Retrieve the 5-day forecast
    forecast_url = "https://api.open-meteo.com/v1/forecast"

    forecast_params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,weather_code",
        "forecast_days": 5,
        "timezone": "auto",
    }

    forecast_data = fetch_api_data(forecast_url, forecast_params)

    daily = forecast_data.get("daily")

    if not daily:
        raise HTTPException(
            status_code=502, detail="Weather service returned incomplete forecast data"
        )
    required_fields = [
        "time",
        "temperature_2m_max",
        "temperature_2m_min",
        "weather_code",
    ]

    if not all(field in daily for field in required_fields):
        raise HTTPException(
            status_code=502, detail="Weather service returned incomplete forecast data"
        )

    if (
        len(
            {
                len(daily["time"]),
                len(daily["temperature_2m_max"]),
                len(daily["temperature_2m_min"]),
                len(daily["weather_code"]),
            }
        )
        != 1
    ):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned inconsistent forecast data",
        )

    # Step 3: Organize the forecast data
    forecast = []

    for i in range(len(daily["time"])):
        day = {
            "date": daily["time"][i],
            "max_temperature": daily["temperature_2m_max"][i],
            "min_temperature": daily["temperature_2m_min"][i],
            "weather_code": daily["weather_code"][i],
            "weather_description": get_weather_description(daily["weather_code"][i]),
        }

        forecast.append(day)

    # Step 4: Return the result
    return {
        "city": location["name"],
        "country": location["country"],
        "forecast": forecast,
    }
