# Architecture Overview

VegetationFLOW has two major components:

- **vegetationflow-core**: The standalone processing and handling satelitte and geospatial data library 

- **tool/**: A user-friendly web app that wraps the core into a web tool

## System Diagram
See `design_docs/system_architecture.png`.

## Component Breakdown

### `core/`
- Pure Python module
- Can be used standalone (`pip install -e ./core`)
- Handles dataset downloading, image processing, dataset loading, vegetation index logic, model training and evaluation.

### `tool/`
- `FastAPI`: Backend for triggering long-running tasks
- `Celery + Redis`: Async task queue to handle processing time consuming tasks like downloading, and training models. 
- `Streamlit`: Frontend interface to interact with data pipeline and maps
- `Docker` : Containerised using `docker-compose`

## Communication Flow

1. User initiates task in Streamlit
2. FastAPI endpoint queues job via Redis and Celery
3. Worker calls `vegetationflow_core` processing functions
4. Results streamed or saved