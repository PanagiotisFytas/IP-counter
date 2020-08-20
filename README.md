# IP-counter
A microservice for counting unique IP addresses

# Requirements

In order to install the required python packages run:

```bash
pip install -r requirements.txt
```

# Starting the service

Start the service by running:

```bash
cd src
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn main:app --reload --port 5000
```

# Endpoints

- For the unique visitor count (not yet implemented) the endpoint is http://localhost:5000/visitors
- For the logging a new vistit (not yet implemented) the endpoint is http://localhost:5000/logs

# Testing API

- In order to run the API unitests run:

```bash
pytest
```