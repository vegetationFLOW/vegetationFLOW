"""
Water Masking Utilities

This module contains functions to generate water masks from satellite imagery
using Google Earth Engine (EE). These masks help separate water pixels from
non-water pixels.

Functions:
----------
- QA_water_mask(image: ee.ImageCollection) -> ee.ImageCollection
    Applies a mask to remove water pixels using the QA_PIXEL band from the input image collection.
"""

import ee

def QA_water_mask(image: ee.ImageCollection) -> ee.ImageCollection:
    """
    Masks out water pixels from an Earth Engine ImageCollection using the QA_PIXEL band.

    The function assumes the 'QA_PIXEL' band contains bit flags, where bit 7 indicates water presence.
    Pixels flagged as water (bit 7 = 1) are masked out (removed).

    Parameters
    ----------
    image : ee.ImageCollection
        The input ImageCollection from which water pixels should be masked out.

    Returns
    -------
    ee.ImageCollection
        A masked ImageCollection with water pixels removed.

    Example
    -------
    >>> collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    >>> masked = QA_water_mask(collection)
    """
    
    qa = image.select('QA_PIXEL')
    water_bit_mask = 1 << 7  # bit 7 = water
    non_water_mask = qa.bitwiseAnd(water_bit_mask).eq(0)  # Keep pixels where water bit is 0 (non-water)

    return image.updateMask(non_water_mask)
