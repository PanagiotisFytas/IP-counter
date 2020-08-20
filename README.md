# IP-counter
A microservice for counting unique IP addresses

# Endpoints

- *GET*: For the getting unique visitor count  the endpoint is http://localhost:5000/visitors
- *POST*: For logging a new visit the endpoint is http://localhost:5000/logs. The api accepts json messages of
the following format:

```json
{ "timestamp": "2020-06-24T15:27:00.123456Z", "ip": "83.150.59.250", "url": ... }
```

## Running the service
### Requirements

In order to install the required python packages run:

```bash
pip install -r requirements.txt
```

### Starting the service

Start the service by running:

```bash
cd src
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn main:app --reload --port 5000
```

### Testing API

- In order to run the unitests run:

```bash
pytest
```

