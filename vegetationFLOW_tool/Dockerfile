FROM python:3.11

WORKDIR /app

# Install system packages needed for geospatial deps
RUN apt-get update && apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    libproj-dev \
    proj-data \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

# Set GDAL environment variables so pip/geopandas can find headers
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Copy dependency files early to leverage Docker layer caching
COPY vegetationFLOW_tool/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project after deps
COPY vegetationFLOW_core /app/vegetationFLOW_core
COPY vegetationFLOW_tool /app/vegetationFLOW_tool
COPY setup.py /app/setup.py

# Install core package in editable mode
RUN pip install --no-cache-dir --use-pep517 -e .