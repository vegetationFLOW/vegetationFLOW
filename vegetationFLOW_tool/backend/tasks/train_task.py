from worker import celery_app
import time


@celery_app.task(name="tasks.download_task.downloadImages")
def training():
    for i in range(10):
        time.sleep(5)
    return "Trained"