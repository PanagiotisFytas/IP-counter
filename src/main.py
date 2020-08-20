from pydantic import BaseModel
from ipaddress import IPv4Address
from fastapi import FastAPI, Request, Response
from datasink import DataSink

class Item(BaseModel):
    timestamp: str
    ip: str
    url: str


CACHE_SIZE = 10000
app = FastAPI()
app.state.sink = DataSink(max_cache_size=CACHE_SIZE)


@app.post("/logs", status_code=200)
def post_log_message(item: Item, request: Request, response: Response):
    try:
        request.app.state.sink.write(item.ip) # write the ip address in the data sink
        msg = {"message": "IP registered", "ip": item.ip}
    except Exception as e:
        msg = {"message": "POST Request failed", "error message": str(e)}
        response.status_code = 500 # Internal Server Error
    return msg


@app.get("/visitors", status_code=200)
def get_count(request: Request, response: Response):
    try:
        cnt = app.state.sink.get_unique_addresses_counter()
        msg = {"Unique IP addresses": cnt}
    except Exception as e:
        msg =  {"message": "GET Request failed", "error message": str(e)}
        response.status_code = 500 # Internal Server Error
    return msg