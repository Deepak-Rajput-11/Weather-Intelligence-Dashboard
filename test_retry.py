import httpx
import pytest
from fastapi import HTTPException
from unittest.mock import patch
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_retries_after_server_error():
    request = httpx.Request("GET", "https://example.com")

    failed_response = httpx.Response(500, request=request)
    successful_response = httpx.Response(
        200,
        json={"ok": True},
        request=request,
    )

    with patch(
        "main.httpx.get",
        side_effect=[failed_response, successful_response],
    ) as mock_get, patch("main.time.sleep"):
        result = main.fetch_api_data("https://example.com", {})

    assert result == {"ok": True}
    assert mock_get.call_count == 2


def test_network_failure_retries_three_times():
    request = httpx.Request("GET", "https://example.com")
    error = httpx.ConnectError("connection failed", request=request)

    with patch(
        "main.httpx.get",
        side_effect=error,
    ) as mock_get, patch("main.time.sleep"):
        with pytest.raises(HTTPException) as exc:
            main.fetch_api_data("https://example.com", {})

    assert exc.value.status_code == 503
    assert mock_get.call_count == 3


def test_client_error_does_not_retry():
    request = httpx.Request("GET", "https://example.com")
    response = httpx.Response(404, request=request)

    with patch("main.httpx.get", return_value=response) as mock_get:
        with pytest.raises(HTTPException) as exc:
            main.fetch_api_data("https://example.com", {})

    assert exc.value.status_code == 502
    assert mock_get.call_count == 1


def test_forecast_rejects_missing_daily_data():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value={},
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_forecast("London")

    assert exc.value.status_code == 502


def test_forecast_rejects_missing_required_field():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    incomplete_data = {
        "daily": {
            "time": ["2026-10-30"],
            "temperature_2m_max": [18],
            "temperature_2m_min": [12],
            # weather_code is intentionally missing
        }
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=incomplete_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_forecast("London")

    assert exc.value.status_code == 502


def test_forecast_rejects_inconsistent_data_lengths():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    incomplete_data = {
        "daily": {
            "time": ["2026-10-30", "2026-10-31"],
            "temperature_2m_max": [18],
            "temperature_2m_min": [12, 11],
            "weather_code": [1, 2],
        }
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=incomplete_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_forecast("London")

    assert exc.value.status_code == 502


def test_weather_rejects_invalid_api_response():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=[25, 60, 12],
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_weather("London")

    assert exc.value.status_code == 502


def test_weather_rejects_invalid_current_data():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    invalid_weather_data = {"current": [25, 60, 12]}

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=invalid_weather_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_weather("London")

    assert exc.value.status_code == 502


def test_weather_rejects_missing_required_field():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    invalid_weather_data = {
        "current": {"temperature_2m": 25, "relative_humidity_2m": 60, "weather_code": 1}
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=invalid_weather_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_weather("London")

    assert exc.value.status_code == 502


def test_weather_rejects_non_numeric_values():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    invalid_weather_data = {
        "current": {
            "temperature_2m": None,
            "relative_humidity_2m": 60,
            "wind_speed_10m": 12,
            "weather_code": 1,
        }
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=invalid_weather_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_weather("London")

    assert exc.value.status_code == 502


def test_forecast_rejects_non_list_data():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    invalid_forecast_data = {
        "daily": {
            "time": ["2026-10-31", "2026-11-01"],
            "temperature_2m_max": "25",
            "temperature_2m_min": [15, 16],
            "weather_code": [1, 2],
        }
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=invalid_forecast_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_forecast("London")

    assert exc.value.status_code == 502


def test_forecast_rejects_non_numeric_values():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    invalid_forecast_data = {
        "daily": {
            "time": ["2026-10-31", "2026-11-01"],
            "temperature_2m_max": [25, "invalid"],
            "temperature_2m_min": [15, 16],
            "weather_code": [1, 2],
        }
    }

    with patch(
        "main.get_city_location",
        return_value=location,
    ), patch(
        "main.fetch_api_data",
        return_value=invalid_forecast_data,
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_forecast("London")

    assert exc.value.status_code == 502


def test_geocoding_rejects_invalid_api_response():
    with patch("main.fetch_api_data", return_value=["invalid"]):
        with pytest.raises(HTTPException) as exc:
            main.get_city_location("London")

    assert exc.value.status_code == 502


def test_geocoding_rejects_invalid_result_structure():
    with patch(
        "main.fetch_api_data",
        return_value={"results": ["invalid"]},
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_city_location("London")

    assert exc.value.status_code == 502


def test_geocoding_returns_valid_location():
    location = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "name": "London",
        "country": "United Kingdom",
    }

    with patch(
        "main.fetch_api_data",
        return_value={"results": [location]},
    ):
        result = main.get_city_location("London")

    assert result == location


def test_geocoding_rejects_missing_required_field():
    location = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "name": "London",
        # country is missing
    }

    with patch(
        "main.fetch_api_data",
        return_value={"results": [location]},
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_city_location("London")

    assert exc.value.status_code == 502


def test_geocoding_rejects_non_numeric_coordinates():
    location = {
        "latitude": "invalid",
        "longitude": -0.1278,
        "name": "London",
        "country": "United Kingdom",
    }

    with patch(
        "main.fetch_api_data",
        return_value={"results": [location]},
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_city_location("London")

    assert exc.value.status_code == 502


def test_geocoding_rejects_empty_location_text():
    location = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "name": "",
        "country": "United Kingdom",
    }

    with patch(
        "main.fetch_api_data",
        return_value={"results": [location]},
    ):
        with pytest.raises(HTTPException) as exc:
            main.get_city_location("London")

    assert exc.value.status_code == 502


def test_server_error_retries_three_times():
    request = httpx.Request("GET", "https://example.com")

    failed_responses = [httpx.Response(500, request=request) for _ in range(3)]

    with patch(
        "main.httpx.get",
        side_effect=failed_responses,
    ) as mock_get, patch("main.time.sleep"):
        with pytest.raises(HTTPException) as exc:
            main.fetch_api_data("https://example.com", {})

    assert exc.value.status_code == 502
    assert mock_get.call_count == 3


def test_invalid_json_response():
    request = httpx.Request("GET", "https://example.com")

    invalid_response = httpx.Response(
        200,
        text="This is not valid JSON",
        request=request,
    )

    with patch(
        "main.httpx.get",
        return_value=invalid_response,
    ) as mock_get:
        with pytest.raises(HTTPException) as exc:
            main.fetch_api_data("https://example.com", {})

    assert exc.value.status_code == 502
    assert mock_get.call_count == 1


def test_weather_endpoint_returns_valid_data():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    weather_data = {
        "current": {
            "temperature_2m": 18.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.0,
            "weather_code": 1,
        }
    }

    with patch("main.get_city_location", return_value=location), patch(
        "main.fetch_api_data",
        return_value=weather_data,
    ):
        response = client.get("/weather", params={"city": "London"})

    assert response.status_code == 200
    assert response.json()["city"] == "London"
    assert response.json()["temperature"] == 18.5
    assert response.json()["humidity"] == 65
    assert response.json()["wind_speed"] == 12.0
    assert response.json()["weather_description"] == "Mainly clear"


def test_forecast_endpoint_returns_valid_data():
    location = {
        "latitude": 51.5,
        "longitude": -0.1,
        "name": "London",
        "country": "United Kingdom",
    }

    forecast_data = {
        "daily": {
            "time": [
                "2026-11-03",
                "2026-11-04",
                "2026-11-05",
                "2026-11-06",
                "2026-11-07",
            ],
            "temperature_2m_max": [18, 19, 17, 16, 20],
            "temperature_2m_min": [12, 13, 11, 10, 14],
            "weather_code": [1, 2, 3, 61, 0],
        }
    }

    with patch("main.get_city_location", return_value=location), patch(
        "main.fetch_api_data",
        return_value=forecast_data,
    ):
        response = client.get("/forecast", params={"city": "London"})

    assert response.status_code == 200
    assert response.json()["city"] == "London"
    assert len(response.json()["forecast"]) == 5
    assert response.json()["forecast"][0]["max_temperature"] == 18
    assert response.json()["forecast"][0]["min_temperature"] == 12
    assert response.json()["forecast"][0]["weather_description"] == "Mainly clear"


def test_weather_endpoint_returns_city_not_found():
    with patch(
        "main.get_city_location",
        side_effect=HTTPException(
            status_code=404,
            detail="City not found",
        ),
    ):
        response = client.get("/weather", params={"city": "InvalidCity"})

    assert response.status_code == 404
    assert response.json()["detail"] == "City not found"


def test_weather_endpoint_rejects_missing_city():
    response = client.get("/weather")

    assert response.status_code == 422


def test_weather_endpoint_rejects_short_city_name():
    response = client.get("/weather", params={"city": "A"})

    assert response.status_code == 422


def test_weather_endpoint_rejects_long_city_name():
    long_city_name = "A" * 101

    response = client.get(
        "/weather",
        params={"city": long_city_name},
    )

    assert response.status_code == 422


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
