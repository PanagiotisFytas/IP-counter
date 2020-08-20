# IP-counter
A microservice for counting unique IP addresses

## Endpoints

- *GET*: For the getting unique visitor count  the endpoint is http://localhost:5000/visitors. The return on a get is json message with the following format:
```json
{"Unique IP addresses": "5"}
```
- *POST*: For logging a new visit the endpoint is http://localhost:5000/logs. The api accepts json messages of
the following format:

```json
{ "timestamp": "2020-06-24T15:27:00.123456Z", "ip": "83.150.59.250", "url": "..." }
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

### Testing the API

In order to run the unitests run:

```bash
pytest
```
### Benchmarking the API

#### Generating URLS

In order to generate multiple POST request (to be used for benchmarking with `siege`) run the following script (located in the `src` folder):

```bash
python url_generator.py > /path/to/url_files.txt
```

Do not forget to replace the path above with an actual path.

This number of requests with unique IP addresses can be specified from the `number_of_requests` static variable from within the script.

### Installing siege

Install siege with the following command for ubuntu:

```bash
sudo apt-get install siege
```






