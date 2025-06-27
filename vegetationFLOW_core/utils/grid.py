import geopandas as gpd
from shapely.geometry import box
import numpy as np
from typing import Union
import math
from pyproj import CRS

def create_grid(
    bounds: Union[np.ndarray, list[float]], 
    cell_size: int, 
    resolution_m: int, 
    crs: CRS | None
) -> gpd.GeoDataFrame:
    """
    Create a uniform grid (vector-based) over a specified bounding box.

    Each cell in the grid will be a square polygon with a size defined 
    by cell_size * resolution_m (in coordinate units).

    Args:
        bounds (Union[np.ndarray, list[float]]): 
            A 1D array or list containing [minx, miny, maxx, maxy] coordinates.
        cell_size (int): 
            The number of pixels along one side of a square cell.
        resolution_m (int): 
            The spatial resolution in meters per pixel. For example, 
            resolution_m = 30 means each pixel represents 30 meters.
        crs (CRS | None): 
            The coordinate reference system for the output grid. Should be a pyproj.CRS 
            object or anything accepted by GeoDataFrame.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the grid polygons with the specified CRS.
    """
    minx, miny, maxx, maxy = bounds
    width = cell_size * resolution_m
    height = cell_size * resolution_m

    # Snap bounds to the grid
    minx = math.floor(minx / width) * width
    miny = math.floor(miny / height) * height
    maxx = math.ceil(maxx / width) * width
    maxy = math.ceil(maxy / height) * height

    cols = np.arange(minx, maxx, width)
    rows = np.arange(miny, maxy, height)

    grid_cells = [box(x, y, x + width, y + height) for x in cols for y in rows]

    grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=crs)
    return grid


def patch_roi(
    roi: gpd.GeoDataFrame, 
    tile_size_px: int, 
    res_m: int
) -> gpd.GeoDataFrame:
    """
    Divides a given Region of Interest (ROI) into spatial tiles (patches) based on 
    a specified tile size and resolution.

    This function:
    1. Reprojects the ROI to EPSG:3857 (meters) for accurate tiling.
    2. Creates a regular grid covering the entire extent of the ROI.
    3. Clips the grid using a spatial join to include only the intersecting tiles.

    Args:
        roi (gpd.GeoDataFrame): 
            A GeoDataFrame representing the region of interest. Should have a valid geometry and CRS.
        tile_size_px (int): 
            Number of pixels per tile side (e.g., 256). Combined with `res_m`, defines patch size in meters.
        res_m (int): 
            Resolution in meters per pixel. E.g., res_m = 10 means each pixel represents 10 meters on ground.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the grid patches that intersect the ROI.
    """
    roi = roi.to_crs(epsg=3857) # Reprojecting to EPSG:3857 (meters) for accurate tiling
    grid = create_grid(
        bounds=roi.total_bounds,
        cell_size=tile_size_px,
        resolution_m=res_m,
        crs=roi.crs
    )
    # Clipping grid to ROI using spatial join
    clipped_tiles = gpd.sjoin(grid, roi, how='inner', predicate='intersects')
    clipped_tiles = clipped_tiles.reset_index(drop=True)
    return clipped_tiles