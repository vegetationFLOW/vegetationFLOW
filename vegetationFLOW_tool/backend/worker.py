from celery import Celery
import ee
import google.auth
import os

def initialize_earth_engine():
    credentials, _ = google.auth.load_credentials_from_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/earthengine.readonly"]
    )
    ee.Initialize(credentials)

try:
    initialize_earth_engine()
    print("Earth Engine initialized in worker!")

except Exception as e:
    print(f"An unexpected error occurred: {e}")


celery_app = Celery(
    "vegetationFLOW_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
    include=["tasks.download_task"]
)

celery_app.conf.task_routes = {
    "tasks.download_task.*": {"queue": "download"},
    "tasks.train_task.*": {"queue": "train"},
}

celery_app.autodiscover_tasks(["tasks"])

