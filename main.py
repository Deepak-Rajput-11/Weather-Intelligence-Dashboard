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

    if not isinstance(geo_data, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid location data",
        )

    results = geo_data.get("results")

    if results is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    if not isinstance(results, list) or not results:
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid location data",
        )

    location = results[0]

    if not isinstance(location, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid location data",
        )

    required_fields = ["latitude", "longitude", "name", "country"]

    if not all(field in location for field in required_fields):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned incomplete location data",
        )

    return location


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/weather")
def get_weather(
    city: str = Query(
        min_length=2,
        max_length=100,
        pattern=r".*\S.*",
        strip_whitespace=True,
    )
) -> dict:

    # Step 1: Find the city
    location = get_city_location(city)

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Fetch current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
    }

    weather_data = fetch_api_data(weather_url, weather_params)

    if not isinstance(weather_data, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid response data",
        )

    current_weather = weather_data.get("current")

    if not isinstance(current_weather, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid current weather data",
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

    temperature_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
    ]

    if not all(
        isinstance(current_weather[field], (int, float))
        and not isinstance(current_weather[field], bool)
        for field in temperature_fields
    ):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid current weather data",
        )

    if not isinstance(current_weather["weather_code"], int) or isinstance(
        current_weather["weather_code"], bool
    ):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid weather code",
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
def get_forecast(
    city: str = Query(
        min_length=2,
        max_length=100,
        pattern=r".*\S.*",
        strip_whitespace=True,
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

    if not isinstance(forecast_data, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid response data",
        )

    daily = forecast_data.get("daily")

    # Step 3: Validate daily data
    if not isinstance(daily, dict):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid forecast data",
        )

    required_fields = [
        "time",
        "temperature_2m_max",
        "temperature_2m_min",
        "weather_code",
    ]

    if not all(field in daily for field in required_fields):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned incomplete forecast data",
        )

    # Step 4: Validate field types
    if not all(isinstance(daily[field], list) for field in required_fields):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid forecast data",
        )

    # Step 5: Reject empty forecast data
    if not daily["time"]:
        raise HTTPException(
            status_code=502,
            detail="Weather service returned empty forecast data",
        )

    # Step 6: Validate numeric values
    temperature_fields = [
        "temperature_2m_max",
        "temperature_2m_min",
    ]

    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for field in temperature_fields
        for value in daily[field]
    ):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid forecast temperatures",
        )

    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in daily["weather_code"]
    ):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid forecast weather codes",
        )

    # Step 7: Validate dates
    if not all(isinstance(value, str) and value.strip() for value in daily["time"]):
        raise HTTPException(
            status_code=502,
            detail="Weather service returned invalid forecast dates",
        )

    # Step 8: Check matching list lengths
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

    # Step 9: Organize forecast data
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

    # Step 10: Return the result
    return {
        "city": location["name"],
        "country": location["country"],
        "forecast": forecast,
    }
