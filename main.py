import time
import uvicorn
from pyzbar import pyzbar
from PIL import Image
import urllib.request
from pydantic import BaseModel, AnyHttpUrl

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


@app.post("/extract")
def extract_qr(inp: PostIn):
    urllib.request.urlretrieve(
        inp.url,
        "gfg.png",
    )
    image = Image.open("gfg.png")
    return pyzbar.decode(image)
