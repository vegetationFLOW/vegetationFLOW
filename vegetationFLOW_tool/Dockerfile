FROM python:3.11-slim

WORKDIR /app

# Copy core package and tool code from the root context
COPY vegetationFLOW_core /app/vegetationFLOW_core
COPY vegetationFLOW_tool /app/vegetationFLOW_tool
COPY setup.py /app/setup.py
COPY vegetationFLOW_tool/requirements.txt /app/requirements.txt

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install the core package in editable mode (pip looks for setup.py in /app)
RUN pip install --use-pep517 -e .

