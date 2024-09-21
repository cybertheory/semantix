from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Semantix"}

def test_subscribe():
    response = client.post("/subscribe/", json={"user_id": "testuser", "user_query": "test query"})
    assert response.status_code == 200
    assert "subscribed" in response.json()["message"]

def test_publish():
    response = client.post("/publish/", json={"notification_text": "Test notification"})
    assert response.status_code == 200
    assert "processed" in response.json()["message"]
