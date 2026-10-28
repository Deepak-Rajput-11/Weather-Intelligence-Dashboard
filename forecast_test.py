import httpx

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 28.61,
    "longitude": 77.21,
    "daily": "temperature_2m_max,temperature_2m_min",
    "forecast_days": 5,
    "timezone": "auto",
}

response = httpx.get(url, params=params, timeout=10.0)
response.raise_for_status()

data = response.json()

daily = data["daily"]

forecast = []

for i in range(len(daily["time"])):
    day = {
        "date": daily["time"][i],
        "max_temperature": daily["temperature_2m_max"][i],
        "min_temperature": daily["temperature_2m_min"][i],
    }

    forecast.append(day)

for day in forecast:
    print(day)
