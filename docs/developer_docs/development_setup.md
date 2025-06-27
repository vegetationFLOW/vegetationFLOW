# Development Setup

## 1. Install Core Locally
```bash
pip install -e ./vegetationFLOW_core
```

## 2A. Local Development of Tool (if Docker not installed)
```bash
cd vegetationFLOW_tool
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run ui.py
```

## 2B. With Docker
Make sure Docker and Docker Compose are installed.
```bash
cd vegetationFLOW_tool
docker-compose up --build
```

