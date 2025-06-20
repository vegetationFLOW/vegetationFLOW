# setup.py tells Python how to install your veg_core package: 
# pip install -e 
# Run the cmd from the root dir, which holds this script

from setuptools import setup, find_packages

setup(
    name='vegetationFLOW_core',
    version='0.1.0',
    packages=find_packages(include=['vegetationFLOW_core', 'vegetationFLOW_core.*']),
    install_requires=[
        'numpy',
        'rasterio',
        'torch',  # or torch, depending on what you use
        'torchvision',
        'scikit-learn',
        'matplotlib',
        'pandas',
        'earthengine-python'
        # add other required core libs
    ],
    python_requires='>=3.8',
    author='Yashna Kumar and Sally Paing',
    author_email='p4p.vegetationflow@gmail.com',
    description='Modular pipeline for vegetation assessment using Remote Sensing, Multispectral Data and Deep Learning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vegetationFLOW/p4p_work',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',          # The project is in early development
        'Intended Audience :: Developers',          # Aimed at developers (not general users)
        'Topic :: Scientific/Engineering :: GIS',   # The project relates to GIS / remote sensing
        'License :: OSI Approved :: MIT License',   # It's open source and uses the MIT license
        'Programming Language :: Python :: 3.8',    # Supports Python 3.8
        'Programming Language :: Python :: 3.9',    # Supports Python 3.9
    ],
    include_package_data=True,
)
