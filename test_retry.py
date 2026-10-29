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
