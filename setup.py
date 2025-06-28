"""
setup.py tells Python how to install your veg_core package: 

pip install -e . --use-pep517
- Use the PEP 517 build process (which involves a pyproject.toml file describing the build system)
- Build your package via the build backend specified in pyproject.toml (like setuptools, Poetry, Flit)
- Avoid running setup.py directly — instead, it calls a standardized interface to build your package.

Run the cmd from the root dir, which holds this script
"""

from setuptools import setup, find_packages

# Gracefully handle missing README.md
try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name='vegetationFLOW_core',
    version='0.1.0',
    packages=find_packages(include=['vegetationFLOW_core', 'vegetationFLOW_core.*']),
    install_requires=[
        'numpy',
        'rasterio',
        'torch',
        'torchvision',
        'scikit-learn',
        'matplotlib',
        'pandas',
        'earthengine-api',
        'shapely',
        'geopandas',
    ],
    python_requires='>=3.8',
    author='Yashna Kumar and Sally Paing',
    author_email='p4p.vegetationflow@gmail.com',
    description='Modular pipeline for vegetation assessment using Remote Sensing, Multispectral Data and Deep Learning',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vegetationFLOW/vegetationFLOW',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    include_package_data=True,
)
