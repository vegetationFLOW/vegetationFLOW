from celery import Celery

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

