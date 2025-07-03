from worker import celery_app
from vegetationFLOW_core import LandsatDownloader
import os

@celery_app.task()
def downloadImages(datasetName:str, roi:str, patchSize:int, startYear:int, endYear:int):
    dwnloader = LandsatDownloader(
        data_dir=os.path.join("/app", "vegetationFLOW_tool", "data"),
        dataset_name=datasetName,
        img_size=patchSize
    )
    if dwnloader.startDownload(roi, startYear, endYear):
        return "Downloaded"
    else:
        return "Not Downloaded"
