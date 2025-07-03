"""
Cloud Masking Utilities

This module contains functions to generate cloud and cloud shadow masks 
from satellite imagery using Google Earth Engine (EE).

Functions:
----------
- QA_cloud_mask(image: ee.ImageCollection) -> ee.ImageCollection
    Applies a mask to remove cloud and cloud shadow pixels using the QA_PIXEL band 
    from the input image collection.
"""

import ee

def QA_cloud_mask(image: ee.ImageCollection) -> ee.ImageCollection:
    """
    Masks out cloud and cloud shadow pixels from an Earth Engine ImageCollection 
    using the QA_PIXEL band.

    The function assumes the 'QA_PIXEL' band contains bit flags where:
      - Bit 3 indicates cloud presence.
      - Bit 11 indicates cloud shadow presence.

    Pixels flagged as cloud or cloud shadow are masked out (removed).

    Parameters
    ----------
    image : ee.ImageCollection
        The input ImageCollection from which cloud and shadow pixels should be masked out.

    Returns
    -------
    ee.ImageCollection
        A masked ImageCollection with cloud and cloud shadow pixels removed.

    Example
    -------
    >>> collection = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
    >>> masked = QA_cloud_mask(collection)
    """
    qa = image.select('QA_PIXEL')
    cloudBit_mask = 1 << 3  # bit 3 = cloud
    shawdowBit_mask = 1 << 11  # bit 4 = cloud shadow
    mask = qa.bitwiseAnd(cloudBit_mask).eq(0).And(qa.bitwiseAnd(shawdowBit_mask).eq(0))
    return image.updateMask(mask)
