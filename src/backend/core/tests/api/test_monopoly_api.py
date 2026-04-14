"""Tests for Monopoly command API endpoint."""

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_monopoly_command_api_returns_parser_output():
    """The endpoint should parse and return a bot response string."""
    client = APIClient()

    response = client.post(
        "/api/v1.0/monopoly/command/",
        {"text": "RUE paix"},
        format="json",
    )

    assert response.status_code == HTTP_200_OK
    payload = response.json()
    assert "response" in payload
    assert "Rue de la Paix" in payload["response"]
    assert "Prix 400M" in payload["response"]


def test_monopoly_command_api_rejects_missing_text():
    """The endpoint should validate that the text field exists."""
    client = APIClient()

    response = client.post(
        "/api/v1.0/monopoly/command/",
        {},
        format="json",
    )

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Le champ 'text' est requis."}
