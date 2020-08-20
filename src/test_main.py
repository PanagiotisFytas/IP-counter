from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

test_request = { "timestamp": "2020-06-24T15:27:00.123456Z", 
                     "ip": "83.150.59.250", 
                     "url": "some/url" 
               }
    
ip_to_test = ["83.150.59.250", "83.150.59.251", "83.150.59.250", "83.150.59.250"
              "83.150.59.252", "83.150.59.251"]

def test_post_log_message():
    response = client.post("/logs", json=test_request)
    assert response.status_code == 200
    assert response.json() == {"message": "IP registered", "ip": "83.150.59.250"}

def test_get_count():
    response = client.get("/visitors")
    assert response.status_code == 200
    assert response.json() == {"Unique IP addresses": 1}

    for ip in ip_to_test:
        test_request['ip'] = ip
        response = client.post("/logs", json=test_request)
        assert response.status_code == 200
        assert response.json() == {"message": "IP registered", "ip": ip}


    response = client.get("/visitors")
    assert response.status_code == 200
    assert response.json() == {"Unique IP addresses": 3}

