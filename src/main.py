from pydantic import BaseModel
from ipaddress import IPv4Address
from fastapi import FastAPI

class Item(BaseModel):
    timestamp: str
    ip: IPv4Address
    url: str

app = FastAPI()

@app.post("/logs", status_code=201)
def post_log_message(item: Item):
    return {'message': 'IP registered', 'ip': item.ip}


@app.get("/visitors", status_code=200)
def get_count():
    return {"non_unique_count": 0}