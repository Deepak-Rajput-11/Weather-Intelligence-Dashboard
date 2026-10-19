# 🌤️ Weather Intelligence Dashboard

A Python-based weather dashboard developed using **FastAPI**, with a frontend planned using HTML, CSS, and JavaScript.

## 📌 About the Project

Weather Intelligence Dashboard is a backend-focused web application currently under development.

The application aims to allow users to search for cities, retrieve current weather information, view forecasts, and explore weather data through an interactive dashboard.

The primary focus is Python backend development, REST APIs, HTTP communication, external API integration, and practical software engineering.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **HTTP Client:** HTTPX
- **Weather API:** Open-Meteo
- **Frontend (Planned):** HTML, CSS, JavaScript
- **Version Control:** Git and GitHub

## ✨ Features

### Implemented Features

- Initialized the FastAPI backend.
- Created a home endpoint (`GET /`).
- Implemented a basic health-check endpoint (`GET /health`).
- Automatic interactive API documentation using FastAPI.
- Integrated the Open-Meteo API to retrieve current weather information.
- Created a weather endpoint (`GET /weather`) for Delhi.
- Retrieved temperature, humidity, and wind speed from an external API.
- Implemented dynamic weather search using city names.
- Integrated Open-Meteo's Geocoding API to convert city names into coordinates.
- Added HTTP 404 error handling for cities that cannot be found.
- Added human-readable weather descriptions using WMO weather codes.
- Implemented reusable HTTP request handling for external APIs.
- Added error handling for network failures, request timeouts, and external API HTTP errors.
- Implemented a 5-day weather forecast endpoint (`GET /forecast`).
- Retrieved daily maximum and minimum temperatures using Open-Meteo.
- Organized forecast data into individual daily records.
- Added city-based forecast searching and invalid-city handling.

### Planned Features

- Visualize weather information using charts.
- Develop a responsive web interface.
- Add automated testing and deploy the application.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Deepak-Rajput-11/Weather-Intelligence-Dashboard.git
cd Weather-Intelligence-Dashboard
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment (Windows PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the Development Server

```bash
fastapi dev main.py
```

The backend will run locally at:

`http://127.0.0.1:8000`

## 🔗 API Endpoints

| Method | Endpoint                | Description                                                |
| ------ | ----------------------- | ---------------------------------------------------------- |
| GET    | `/`                     | Returns a welcome message                                  |
| GET    | `/health`               | Returns a basic application health status                  |
| GET    | `/weather?city=London`  | Returns current weather information for the requested city |
| GET    | `/forecast?city=London` | Returns a 5-day weather forecast for the requested city    |

FastAPI's interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## 📅 Development Log

### Day 0 — October 14, 2026 | Project Preparation and Fundamentals

**Concepts Learned:**

- Difference between frontend, backend, and full-stack development.
- Introduction to APIs and HTTP communication.
- Understanding GET, POST, PUT, and DELETE methods.
- Introduction to JSON and HTTP status codes.
- Understanding Python frameworks and FastAPI.
- Introduction to virtual environments, servers, and API endpoints.

**Work Completed:**

- Created the Weather Intelligence Dashboard project folder.
- Created and activated a Python virtual environment.
- Installed FastAPI and its development dependencies.
- Configured the Python interpreter in VS Code.
- Created the initial `main.py` file.
- Initialized the FastAPI application.
- Implemented the first API endpoint (`GET /`).
- Successfully started the backend using Uvicorn.

---

### Day 1 — October 15, 2026 | GitHub Setup and API Development

**Concepts Learned:**

- Git repository initialization and version control.
- Understanding `.gitignore` and excluded files.
- Git staging, commits, remote repositories, and pushing code.
- API routing using FastAPI decorators.
- Health-check endpoints and request-response communication.
- Understanding HTTP 404 errors and basic backend debugging.

**Work Completed:**

- Created `.gitignore` to exclude the virtual environment and unnecessary files.
- Initialized the local Git repository.
- Created the GitHub repository and connected it to the local project.
- Created and pushed the initial commit.
- Implemented the `/health` API endpoint.
- Tested both API endpoints using a browser.
- Created the project README documentation.

---

### Day 2 — October 16, 2026 | External Weather API Integration

**Concepts Learned:**

- Understanding external APIs and HTTP requests using HTTPX.
- Sending GET requests with query parameters.
- Understanding API responses and extracting nested JSON data.
- Integrating external APIs into FastAPI endpoints.
- Understanding request timeouts and HTTP error checking.
- Managing Python project dependencies using `requirements.txt`.

**Work Completed:**

- Installed HTTPX for external API communication.
- Created `weather_test.py` to test Open-Meteo API requests.
- Successfully retrieved real weather information for Delhi.
- Extracted temperature, humidity, and wind speed from the API response.
- Implemented the `GET /weather` endpoint in FastAPI.
- Tested the endpoint successfully in the browser.
- Created `requirements.txt` to document project dependencies.

### Day 3 — October 17, 2026 | Dynamic Weather Search and Geocoding

**Concepts Learned:**

- Understanding query parameters in FastAPI.
- Introduction to geocoding and geographical coordinates.
- Using multiple external APIs within a single backend endpoint.
- Extracting location information from nested JSON responses.
- Understanding HTTP exceptions and handling invalid city names.

**Work Completed:**

- Modified the `/weather` endpoint to accept city names dynamically.
- Created `geocoding_test.py` to experiment with Open-Meteo's Geocoding API.
- Successfully retrieved latitude and longitude using city names.
- Integrated the Geocoding API with the Weather Forecast API.
- Removed hardcoded Delhi coordinates from the weather endpoint.
- Tested weather retrieval for multiple cities.
- Implemented and tested HTTP 404 responses for invalid locations.

---

### Day 4 — October 18, 2026 | Weather Descriptions and API Error Handling

**Concepts Learned:**

- Understanding weather condition codes and their descriptions.
- Mapping numeric codes to readable text using Python dictionaries.
- Using dictionary `.get()` with a default value.
- Handling HTTP request failures using `try` and `except`.
- Understanding HTTP 502 and 503 status codes.
- Creating reusable functions to reduce duplicate code.

**Work Completed:**

- Added `weather_code` to the Open-Meteo weather request.
- Created `get_weather_description()` to convert weather codes into readable descriptions.
- Added `weather_description` to the `/weather` API response.
- Created a reusable `fetch_api_data()` function for external API requests.
- Implemented error handling for connection failures, timeouts, and external API errors.
- Refactored geocoding and weather requests to use the shared helper function.
- Successfully tested weather retrieval and invalid-city handling.

---

### Day 5 — October 19, 2026 | Five-Day Weather Forecast Integration

**Concepts Learned:**

- Understanding daily weather forecasts and forecast API parameters.
- Retrieving maximum and minimum temperatures using Open-Meteo.
- Using `forecast_days` and automatic timezone selection.
- Working with multiple related lists in JSON responses.
- Converting forecast data into a list of dictionaries.
- Reusing existing backend functions for new API endpoints.

**Work Completed:**

- Created `forecast_test.py` to experiment with Open-Meteo's daily forecast API.
- Successfully retrieved five days of forecast information.
- Organized forecast dates and temperatures into individual daily records.
- Implemented the `GET /forecast` endpoint in FastAPI.
- Integrated city geocoding with daily forecast retrieval.
- Reused the existing `fetch_api_data()` helper function.
- Successfully tested forecasts for London and Mumbai.
- Verified HTTP 404 handling for invalid city names.
