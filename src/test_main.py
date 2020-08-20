from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_post_log_message():
    test_request = { "timestamp": "2020-06-24T15:27:00.123456Z", 
                     "ip": "83.150.59.250", 
                     "url": "some/url" 
                   }
    response = client.post("/logs", json=test_request)
    assert response.status_code == 200
    assert response.json() == {"message": "IP registered", "ip": "83.150.59.250"}

def test_get_count():
    response = client.get("/visitors")
    assert response.status_code == 200
    assert response.json() == {"Unique IP addresses": 1}
