import httpx

url = "https://geocoding-api.open-meteo.com/v1/search"

params = {"name": "London", "count": 1, "language": "en", "format": "json"}

response = httpx.get(url, params=params, timeout=10.0)
response.raise_for_status()

data = response.json()

location = data["results"][0]

city = location["name"]
latitude = location["latitude"]
longitude = location["longitude"]
country = location["country"]

print("City:", city)
print("Country:", country)
print("Latitude:", latitude)
print("Longitude:", longitude)
