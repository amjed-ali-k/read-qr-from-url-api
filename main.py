import os
import time
import uvicorn
import requests

from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"URL: {request.url.path} | Process time: {process_time:.2f} seconds"
    )
    return response




@app.post("/extract")
def extract_qr(inp):
    requests.get()
    pass