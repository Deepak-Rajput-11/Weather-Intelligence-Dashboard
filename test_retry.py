import httpx
import pytest
from fastapi import HTTPException
from unittest.mock import patch

import main


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
