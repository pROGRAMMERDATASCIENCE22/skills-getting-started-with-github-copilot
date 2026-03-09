import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app
from fastapi.testclient import TestClient

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), dict)

@pytest.mark.asyncio
async def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@example.com"
    test_activity = None
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Get an activity name
        activities_resp = await ac.get("/activities")
        activities = activities_resp.json()
        if not activities:
            pytest.skip("No activities available to test signup.")
        test_activity = list(activities.keys())[0]

        # Act: Sign up
        signup_resp = await ac.post(f"/activities/{test_activity}/signup?email={test_email}")
        # Assert: Signup
        assert signup_resp.status_code == status.HTTP_200_OK
        assert "message" in signup_resp.json()

        # Act: Unregister
        unregister_resp = await ac.post(f"/activities/{test_activity}/unregister?email={test_email}")
        # Assert: Unregister
        assert unregister_resp.status_code == status.HTTP_200_OK
        assert "message" in unregister_resp.json()
