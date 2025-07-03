# start_worker.py
from worker import celery_app

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start Celery Worker")
    parser.add_argument("--queue", type=str, default="default", help="Celery queue name")
    parser.add_argument("--loglevel", type=str, default="info", help="Logging level")

    args = parser.parse_args()

    celery_app.worker_main([
        "worker",
        "--loglevel", args.loglevel,
        "--queues", args.queue
    ])
