from fastapi import APIRouter
from pydantic import BaseModel
from tasks.download_task import downloadImages

class DownloadInput(BaseModel):
    Dataset_Name: str
    Collection_Type: str
    Start_Year: int
    End_Year: int
    ROI: str
    Patch_Size: int 

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)

@router.post("/start/")
def start_download():
    task = downloadImages.delay()
    return {"task_id": task.id}
