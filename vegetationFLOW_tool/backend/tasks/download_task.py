from worker import celery_app
import time

@celery_app.task()
def downloadImages():
    for i in range(5):
        time.sleep(5)
    return "Downloaded"
