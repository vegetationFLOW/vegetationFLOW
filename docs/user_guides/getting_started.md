# Getting Started with VegetationFLOW

VegetationFLOW is a flexible toolkit for vegetation index computation, fire severity analysis, and interactive remote sensing workflows. You can either:

- Use the **VegetationFLOW-core** Python module directly
- Launch the full **VegetationFLOW Tool** web interface with backend processing and task queue

## 1. Clone the Repository
```bash
git clone https://github.com/your-org/VegetationFLOW.git
cd VegetationFLOW
```

## 2. Run the App (Tool)
```bash
cd tool
docker-compose up --build
```
Access the frontend at: http://localhost:8501

## 3. Use Core as a Python Package
```bash
pip install -e ./core
python -m vegetationflow_core.cli --help
```