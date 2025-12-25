import os

import pytest
from core.urls import api  # Import the Ninja API instance
from django.contrib.auth.models import User
from ninja.testing import TestClient
from ninja_jwt.tokens import RefreshToken


@pytest.fixture
def user(db):
    """Creates a standard user for testing."""
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def auth_client(user):
    """
    Returns a Ninja TestClient with the Auth header already configured.
    This simulates a logged-in user with JWT.
    """
    # 1. Generate the token manually (without calling the login endpoint to be faster)
    os.environ["NINJA_SKIP_REGISTRY"] = "yes"
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # 2. Create the client injecting the token
    client = TestClient(api)
    # Ninja TestClient doesn't handle global headers as easily as DRF,
    # so we make a wrapper or pass the header in each request.
    # For simplicity, we return a tuple (client, headers)
    auth_headers = {"Authorization": f"Bearer {access_token}"}

    return client, auth_headers
