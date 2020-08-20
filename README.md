# IP-counter
A microservice for counting unique IP addresses

# Starting the service

Start the service by running (inside the `src_folder`):

```bash
uvicorn main:app --reload --port 5000
```

# Endpoints

- For the unique visitor count (not yet implemented) the endpoint is http://localhost:5000/visitors
- For the logging a new vistit (not yet implemented) the endpoint is http://localhost:5000/logs