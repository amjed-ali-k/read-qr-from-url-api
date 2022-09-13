from collections import namedtuple
from enum import Enum
import time
from pyzbar import pyzbar
from PIL import Image
import urllib.request
from pydantic import BaseModel, AnyHttpUrl
from typing import List, Union

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"URL: {request.url.path} | Process time: {process_time:.2f} seconds")
    return response


class PostIn(BaseModel):
    url: AnyHttpUrl


class ResModel(BaseModel):
    __root__: List[List[Union[Union[int, str], List[Union[int, List[int]]]]]]


Rect = namedtuple("Rect", ["left", "top", "width", "height"])
Point = namedtuple("Point", ["x", "y"])


class Orientation(str, Enum):
    UNKNOWN = "UNKNOWN"
    UP = "UP"
    RIGHT = "RIGHT"
    DOWN = "DOWN"
    LEFT = "LEFT"


class QRModel(BaseModel):
    data: str
    dataType: str
    rect: Rect
    polygon: List[Point]
    quality: float
    direction: Orientation | str


@app.post("/extract", response_model=List[QRModel])
def extract_qr_from_url(inp: PostIn):
    urllib.request.urlretrieve(
        inp.url,
        "gfg.png",
    )
    image = Image.open("gfg.png")
    decoded = pyzbar.decode(image)
    ret = []
    for item in decoded:
        ret.append(QRModel(*item))
    return ret
