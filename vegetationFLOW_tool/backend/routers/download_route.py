from fastapi import APIRouter
from pydantic import BaseModel
from tasks.download_task import downloadImages
import os
import json
from fastapi import HTTPException

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
def start_download(data: DownloadInput):
    roi_path = os.path.join("/app", "vegetationFLOW_tool", "data", "geojsons", f"{data.Dataset_Name}.geojson")
    os.makedirs(os.path.join("/app", "vegetationFLOW_tool", "data", "geojsons"), exist_ok=True)
    # 👇 Ensure the GeoJSON is properly formatted
    with open(roi_path, "w") as f:
        f.write(data.ROI)
    task = downloadImages.delay(data.Dataset_Name, 
                                roi_path, 
                                data.Patch_Size, 
                                data.Start_Year, 
                                data.End_Year)
    return {"task_id": task.id}
