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
- **Frontend (Planned):** HTML, CSS, JavaScript
- **Weather API (Planned):** Open-Meteo
- **Version Control:** Git and GitHub

## ✨ Features

### Implemented Features

- Initialized the FastAPI backend.
- Created a home endpoint (`GET /`).
- Implemented a basic health-check endpoint (`GET /health`).
- Automatic interactive API documentation using FastAPI.

### Planned Features

- Search weather information by city.
- Retrieve current weather data using an external API.
- Display temperature, humidity, wind speed, and weather conditions.
- Show upcoming weather forecasts.
- Visualize weather information using charts.
- Handle invalid locations and external API errors.
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
python -m pip install "fastapi[standard]"
```

### 5. Start the Development Server

```bash
fastapi dev main.py
```

The backend will run locally at:

`http://127.0.0.1:8000`

## 🔗 API Endpoints

| Method | Endpoint  | Description                               |
| ------ | --------- | ----------------------------------------- |
| GET    | `/`       | Returns a welcome message                 |
| GET    | `/health` | Returns a basic application health status |

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
