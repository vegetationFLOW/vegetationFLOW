from fastapi import FastAPI
import vegetationFLOW_core
import ee
import os
import google.auth
from pydantic import BaseModel
from routers import download_route
from worker import celery_app

glob_var = 0

app = FastAPI()

app.include_router(download_route.router)

@app.get("/task-status/{task_id}")
def get_status(task_id: str):
    res = celery_app.AsyncResult(task_id)  # bind to celery app instance
    return {
        "task_id": task_id,
        "status": res.status,
        "result": res.result if res.successful() else None,
    }