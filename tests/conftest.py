import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the activities dict before each test for isolation
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))

@pytest.fixture
def client():
    return TestClient(app)
