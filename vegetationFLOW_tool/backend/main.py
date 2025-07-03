from fastapi import FastAPI
import vegetationFLOW_core
import ee
import os
import google.auth
from pydantic import BaseModel
from routers import download_route

glob_var = 0

app = FastAPI()

app.include_router(download_route.router)

@app.get("/status/{task_id}")
def start_download(task_id:str):
    global glob_var
    glob_var += 1
    return {"progress": glob_var}