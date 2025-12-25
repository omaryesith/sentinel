import pytest
from domains.models import Domain


# Mark that this test requires database access
@pytest.mark.django_db
def test_create_domain_authorized(auth_client):
    """
    Verifies that an authenticated user can create a domain.
    """
    client, headers = auth_client

    payload = {"name": "Python.org", "url": "https://www.python.org"}

    # Make the POST request passing the JWT headers
    response = client.post("/domains/", json=payload, headers=headers)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Python.org"
    assert data["id"] is not None

    # Verify that it was actually saved in the DB
    assert Domain.objects.count() == 1


@pytest.mark.django_db
def test_create_domain_unauthorized(client):  # Use pytest-django's native 'client'
    """
    Verifies that the API rejects anonymous users (Without Token).
    """
    # Use Django's standard client for a raw request without auth
    response = client.post(
        "/api/domains/",
        data={"name": "Hacker", "url": "https://hack.com"},
        content_type="application/json",
    )

    # Should reject with 401
    assert response.status_code == 401
