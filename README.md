# 🌤️ Weather Intelligence Dashboard

A Python-based weather dashboard built with **FastAPI**, **HTML**, **CSS**, and **JavaScript**, using the Open-Meteo API to retrieve and display real-time weather information and a five-day forecast.

## 📌 About the Project

Weather Intelligence Dashboard is a web application that allows users to search for cities, view current weather conditions, and explore a five-day weather forecast through an interactive web interface.

The project focuses on Python backend development, REST APIs, external API integration, frontend-backend communication, input validation, error handling, and practical software engineering.

## 🛠️ Technologies Used

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **HTTP Client:** HTTPX
- **Weather API:** Open-Meteo
- **Frontend:** HTML, CSS, JavaScript
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
- Added daily weather codes to the five-day forecast response.
- Added human-readable weather descriptions to each forecast day.
- Added city input validation using FastAPI's Query parameters.
- Enforced minimum and maximum city-name lengths for weather and forecast endpoints.
- Tested valid and invalid city inputs.
- Refactored city geocoding into a reusable `get_city_location()` function.
- Removed duplicated geocoding logic from the weather and forecast endpoints.
- Tested both endpoints to confirm existing functionality remains intact.
- Added type hints to helper functions and API endpoints.
- Improved code readability by documenting expected input and return types.
- Tested existing endpoints to verify that functionality remains intact.
- Created the frontend using HTML, CSS, and JavaScript.
- Configured FastAPI to serve the frontend homepage and static files.
- Connected the frontend to the current-weather and forecast API endpoints using JavaScript Fetch.
- Displayed current weather details dynamically on the webpage.
- Rendered five-day forecast data as individual forecast elements.
- Added CSS Grid styling for the forecast layout.
- Added basic frontend error messaging for forecast request failures.

### Planned Features

- Visualize weather information using charts.
- Improve loading states and frontend error handling.
- Complete application testing and validation.
- Polish the user interface and improve accessibility.
- Deploy the application.

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

| Method | Endpoint                | Description                                                                        |
| ------ | ----------------------- | ---------------------------------------------------------------------------------- | --- |
| GET    | `/`                     | Serves the Weather Intelligence Dashboard homepage                                 |     |
| GET    | `/health`               | Returns a basic application health status                                          |
| GET    | `/weather?city=London`  | Returns current weather information for the requested city                         |
| GET    | `/forecast?city=London` | Returns a 5-day forecast with daily high/low temperatures and weather descriptions |

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

---

### Day 6 — October 20, 2026 | Weather Conditions in Five-Day Forecast

**Concepts Learned:**

- Requesting additional daily weather variables from an external API.
- Understanding weather codes returned for multiple forecast days.
- Reusing an existing function to convert numerical codes into readable descriptions.
- Accessing corresponding values from related lists using a loop index.
- Debugging Python indentation and understanding how it affects loop execution.
- Testing API responses for multiple valid cities and invalid city names.

**Work Completed:**

- Added `weather_code` to the daily forecast API request.
- Added `weather_code` and `weather_description` to each daily forecast record.
- Reused `get_weather_description()` to translate forecast codes into readable weather conditions.
- Fixed a loop indentation issue that initially caused only one forecast day to be returned.
- Tested the five-day forecast for London and Mumbai.
- Verified that invalid city names return HTTP 404 with an appropriate error message.
- Confirmed that each forecast day includes its date, maximum temperature, minimum temperature, weather code, and weather description.

### Day 7 — October 21, 2026 | City Input Validation

**Concepts Learned:**

- Using FastAPI's `Query` to validate query parameters.
- Setting minimum and maximum input lengths.
- Understanding HTTP 422 validation errors.
- Testing valid and invalid inputs.

**Work Completed:**

- Imported `Query` from FastAPI.
- Added city-name length validation to the `/weather` endpoint.
- Added city-name length validation to the `/forecast` endpoint.
- Set a minimum length of 2 characters and a maximum length of 100 characters.
- Tested short, empty, and valid city inputs.
- Confirmed that both endpoints continue to work correctly.

### Day 8 — October 22, 2026 | Code Reuse and Geocoding Refactoring

**Concepts Learned:**

- Identifying duplicated code.
- Creating reusable helper functions.
- Refactoring code without changing endpoint behavior.
- Returning and reusing location data across endpoints.

**Work Completed:**

- Created the `get_city_location()` helper function.
- Centralized city geocoding and city-not-found error handling.
- Updated `get_weather()` to use the shared function.
- Updated `get_forecast()` to use the shared function.
- Tested both endpoints with valid and invalid city names.
- Confirmed that existing weather and forecast functionality continues to work.

### Day 9 — October 23, 2026 | Type Hints and Code Readability

**Concepts Learned:**

- Understanding Python parameter type hints.
- Using return type hints to communicate expected return values.
- Applying type hints to helper functions and FastAPI endpoints.
- Understanding that type hints do not automatically enforce types at runtime.

**Work Completed:**

- Added a return type hint to `get_city_location()`.
- Added parameter and return type hints to `fetch_api_data()`.
- Added parameter and return type hints to `get_weather_description()`.
- Added return type hints to `get_weather()` and `get_forecast()`.
- Tested current weather, five-day forecast, invalid city handling, and input validation.
- Confirmed that all four tests passed.

---

### Day 10 — October 24, 2026 | Frontend Integration and Weather Dashboard

**Concepts Learned:**

- Serving HTML files using FastAPI's `FileResponse`.
- Serving static assets using FastAPI's `StaticFiles`.
- Connecting HTML forms to JavaScript event listeners.
- Preventing default form submission using `event.preventDefault()`.
- Fetching backend API data using JavaScript `fetch()`.
- Handling JSON responses and HTTP errors.
- Updating webpage content dynamically using the DOM.
- Rendering forecast data using `forEach()` and dynamically created elements.
- Applying CSS Grid to arrange forecast items.

**Work Completed:**

- Created the frontend HTML structure.
- Added CSS styling for the dashboard.
- Configured FastAPI to serve the homepage and static files.
- Connected the city search form to the `/weather` and `/forecast` endpoints.
- Displayed current weather information dynamically.
- Rendered the five-day forecast on the webpage.
- Added styling for individual forecast items.
- Implemented basic error messaging for forecast request failures.
- Tested the dashboard using a city search.

### Day 11 — October 25, 2026 | Frontend Error Handling and Request Coordination

**Concepts Learned:**

- Coordinating multiple asynchronous requests using `Promise.all()`.
- Handling failed HTTP responses using `response.ok` and HTTP status codes.
- Understanding the difference between HTTP errors and network errors.
- Displaying loading, success, and error states in a frontend.
- Clearing stale data when a new search begins.
- Using JavaScript's `Error` objects and `.catch()` for error handling.

**Work Completed:**

- Coordinated current-weather and five-day forecast requests using `Promise.all()`.
- Added a loading message while weather data is being retrieved.
- Updated the dashboard after both requests succeed.
- Added user-friendly error messages for invalid cities and weather-service failures.
- Preserved HTTP status codes in frontend errors.
- Cleared previous weather and forecast results before starting a new search.
- Tested valid city searches and invalid city handling successfully.

---

### Day 12 — October 26, 2026 | Input Validation and Asynchronous Request Handling

**Concepts Learned:**

- Validating user input with JavaScript's `.trim()`.
- Tracking searches using incrementing request IDs.
- Understanding race conditions in asynchronous JavaScript.
- Using `Promise.all()` to coordinate multiple API requests.
- Preventing stale success and error callbacks from updating the interface.

**Work Completed:**

- Added validation to prevent empty and whitespace-only city searches.
- Assigned an incrementing ID to each valid search.
- Prevented outdated successful requests from overwriting the latest search results.
- Prevented outdated failed requests from replacing the latest search's status message.
- Tested rapid searches, invalid city requests, and responses completing in different orders.

---