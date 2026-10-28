import httpx

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 28.61,
    "longitude": 77.21,
    "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
}

response = httpx.get(url, params=params)

data = response.json()

current_weather = data["current"]

temperature = current_weather["temperature_2m"]
humidity = current_weather["relative_humidity_2m"]
wind_speed = current_weather["wind_speed_10m"]

print("Temperature:", temperature, "°C")
print("Humidity:", humidity, "%")
print("Wind Speed:", wind_speed, "km/h")
