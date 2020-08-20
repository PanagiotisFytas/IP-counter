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

### Storage

A `python shelve` is used as a form of persistent storage. Since we have IPv4 addresses the 
use of persistent storage is not essential: we could use a bit array with a size of `2*32 bits`. That would need
a memory of around 550 MB at all times. However, a persistent storage can alleviate the need for 
so much memory and allow for extending to IPv6 addresses (which cannot be stored in memory).

### Caching

The code offers the ability of caching the POST requests so we do not have to search the
Data Sink (currently a simple `python shelve`) after each individual request. For the `shelve` 
this should no increase the average throughput, since the `shelve` does not offer an option
for batch writing. However, if we change the sink to an actual database the performance increase
of a cache should be considerable.

The size of the cache can be specified by changing the static variable `CACHE_SIZE` inside `main.py`.
In the future this will change from a configuration file.

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

#### Installing siege

Install siege with the following command for ubuntu:

```bash
sudo apt-get install siege
```
#### Running siege

Run siege with the following command:

```bash
siege -f src/urls.txt -t 1M -c 25
```

Where `-t 1M` specifies running the benchmark for 1 minue and `-c 25` specifies 25 concurrent clients


#### Benchmarks

Running siege with `25` concurrent users, for `1` minute and with `max_cache_size=10000` we get the
following output:

```
** SIEGE 4.0.4
** Preparing 50 concurrent users for battle.
The server is now under siege...
Lifting the server siege...
Transactions:                  86839 hits
Availability:                 100.00 %
Elapsed time:                  59.83 secs
Data transferred:               3.77 MB
Response time:                  0.03 secs
Transaction rate:            1451.43 trans/sec
Throughput:                     0.06 MB/sec
Concurrency:                   49.86
Successful transactions:       86839
Failed transactions:               0
Longest transaction:            0.18
Shortest transaction:           0.00
```

Running the same experiment, but *without a cache* produces the following results:

```
** SIEGE 4.0.4
** Preparing 25 concurrent users for battle.
The server is now under siege...
Lifting the server siege...
Transactions:                  88472 hits
Availability:                 100.00 %
Elapsed time:                  59.64 secs
Data transferred:               3.83 MB
Response time:                  0.02 secs
Transaction rate:            1483.43 trans/sec
Throughput:                     0.06 MB/sec
Concurrency:                   24.92
Successful transactions:       88472
Failed transactions:               0
Longest transaction:            0.13
Shortest transaction:           0.00
```

We observe the following:
- In both cases we can easily handle around `1500 transations/sec` with an
fast average response time of `0.02 sec` or `0.03 sec`.
- We observe no improvement in the transaction rate and average response time
when using a cache. The reason for this is that the current data sink (`python shelve`)
does not offer the ability to write batches and therefore there is not performance increase. 
However, the code gives the ability to easily change the datasink. 
For instance, in most databases writing in batches is significantly faster than using multiple
queries that only affect on entry. In that case, we would see an increase in performance using the cache.