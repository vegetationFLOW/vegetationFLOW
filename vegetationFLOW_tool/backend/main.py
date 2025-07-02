from fastapi import FastAPI
import vegetationFLOW_core
import ee
import os
import google.auth
from pydantic import BaseModel

glob_var = 0

app = FastAPI()

class DownloadInput(BaseModel):
    Dataset_Name: str
    Collection_Type: str
    Start_Year: int
    End_Year: int
    ROI: str
    Patch_Size: int 

@app.post("/start-download/")
def start_download(data: DownloadInput):
    return {"task_id": 2}

@app.get("/download-status/{task_id}")
def start_download(task_id:str):
    global glob_var
    glob_var += 1
    return {"progress": glob_var}