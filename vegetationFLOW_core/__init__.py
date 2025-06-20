__version__ = "0.1.0"

""" Example of an Init script; Add modules that are frquently use and to avoid nested imports 
from .datasets import load_images          # example function from data.py
from .models import VegetationModel    # example class from models.py
from .preprocessing import normalize_ndvi  # example function

# Optionally, list what will be imported on 'from veg_core import *'
__all__ = [
    "load_images",
    "VegetationModel",
    "normalize_ndvi",
]

"""