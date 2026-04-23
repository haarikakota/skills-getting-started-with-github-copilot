import pytest

# Arrange-Act-Assert pattern used in all tests

def test_get_activities(client):
    # Arrange: (client fixture provides TestClient)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

def test_signup_success(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

def test_signup_duplicate(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_invalid_activity(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_success(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

def test_unregister_not_signed_up(client):
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_unregister_invalid_activity(client):
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
