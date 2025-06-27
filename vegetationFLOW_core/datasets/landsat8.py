# Imports
import os
import calendar
from datetime import datetime
import requests
from typing import Literal
import concurrent.futures
from vegetationFLOW_core.utils import patch_roi, checkDateRange
from vegetationFLOW_core.preprocessing import QA_water_mask, QA_cloud_mask

import ee
import geopandas as gpd
import shapely
import numpy as np

class LandsatDownloader:
    """
    A utility class for organizing and managing the download process for Landsat satellite imagery 
    using Google Earth Engine.

    This class handles creation of directory structures for saving imagery associated with 
    a given region or dataset name. It assumes Earth Engine has already been authenticated 
    and initialized before use.

    Attributes:
        res_m (int): Spatial resolution of Landsat imagery (default: 30 meters/pixel).
        img_size (int): Landsat image size (default: 256px).
        dataset_dir (str): Full path to the directory where satelitte data will be stored.
    """

    def __init__(self, data_dir: str, dataset_name: str, res_m:int=30, img_size:int=256) -> None:
        """
        Initializes the LandsatDownloader and sets up the folder structure 
        for downloading satellite imagery. 

        Args:
            data_dir (str): 
                Root directory where satellite imagery will be saved. 
                If the directory doesn't exist, it will be created.
            
            dataset_name (str): 
                Name of the specific dataset or region of interest 
                (e.g., "Auckland_NZ"). Used to create a subfolder inside data_dir.

            res_m (int):
                Spatial Resolution of the images to download

            img_size (int):
                Image/Patch Size for the images in pixels
        """

        # Create dataset-specific subdirectory
        self.dataset_dir = os.path.join(data_dir, dataset_name)
        self.res_m = res_m
        self.img_size = img_size

         # Ensure directories exists
        os.makedirs(name=data_dir, exist_ok=True)
        os.makedirs(name=self.dataset_dir, exist_ok=True)
    
    def load_ee_composite(
            self, 
            roi_gdf:gpd.GeoDataFrame, 
            startDate:str, 
            endDate:str
    ) -> ee.Image | None:
        """
        Loads a cloud- and water-masked Landsat 8 median composite Image for a given region and time range,
        applying scaling factors to the optical bands.

        Args:
            roi_gdf (gpd.GeoDataFrame): GeoDataFrame representing the region of interest (ROI). 
                                        Only the first geometry is used.
            startDate (str): Start date of the date range filter, in 'YYYY-MM-DD' format.
            endDate (str): End date of the date range filter, in 'YYYY-MM-DD' format.

        Returns:
            ee.Image | None:    The scaled median composite Image with selected optical bands,
                                or None if no images are found for the specified parameters.
        """
        roi_gdf = roi_gdf.to_crs(epsg=4326) # EE expects geometry in 4326
        roi_ee = ee.Geometry(shapely.geometry.mapping(roi_gdf.geometry.iloc[0]))

        def apply_scale_factors(image):
            optical_bands = image.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7']).multiply(0.0000275).add(-0.2)
            return image.addBands(optical_bands, None, True)

        collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                    .filterBounds(roi_ee)
                    .filterDate(startDate, endDate)
                    .map(QA_cloud_mask)
                    .map(QA_water_mask)
                    )
        if collection.size().getInfo() == 0:
            print("No images found for this region and date.")
            return None
        median_composite = collection.median()
        scaled_composite = apply_scale_factors(median_composite)
        scaled_composite = scaled_composite.select(['SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'])  
        # B, G, R, NIR, SWIR1, SWIR2 => Important, as this is how it will downloaded
        return scaled_composite
    
    def checkTileValidity(
        self, 
        tile_image: ee.ImageCollection, 
        tile_geom_ee: ee.Geometry
    ) -> bool:
        """
        Checks whether a given tile contains a sufficient amount of valid data pixels.

        The validity is assessed by comparing the count of valid pixels in the "SR_B4" band
        within the tile geometry against 10% of the total pixels in that area.

        Args:
            tile_image (ee.ImageCollection): The image collection for the tile, 
                expected to contain the band "SR_B4" with a mask applied indicating valid pixels.
            tile_geom_ee (ee.Geometry): The Earth Engine geometry defining the tile's spatial extent.

        Returns:
            bool: True if the valid pixel count is greater than 10% of total pixels, else False.
        """
        mask = tile_image.select("SR_B4").mask()

        valid_pixels = mask.reduceRegion(
            reducer = ee.Reducer.sum(),
            geometry = tile_geom_ee,
            scale = 30,
        ).get("SR_B4")

        total_pixels = ee.Image.constant(1).clip(tile_geom_ee).reduceRegion(
            reducer=ee.Reducer.count(),
            geometry=tile_geom_ee,
            scale=30
        ).get("constant")

        valid_pixels_val = valid_pixels.getInfo()
        total_pixels_val = total_pixels.getInfo()

        if valid_pixels_val <= 0.1*total_pixels_val: # If true: Invalid data
            return False
        else:
            return True

    def downloadURL(
        self, 
        composite: ee.ImageCollection,
        img_size:int,   
        filepath: str
    ) -> None:
        """
        Downloads a clipped composite image as a GeoTIFF file with specified dimensions and CRS.

        Assumes the input image is already clipped to the region of interest and has a valid geometry.

        Args:
            composite (ee.Image): An Earth Engine Image, already clipped to the target tile.
            img_size (int): Image Size in pixels. Assuming Height and Width is the same
            filepath (str): Local file path where the downloaded GeoTIFF will be saved.

        Raises:
            requests.RequestException: If the HTTP request to download the image fails.
        """
        region_JSON = composite.geometry().getInfo()  # Get clipped image geometry info
        
        url = composite.getDownloadURL({
            'region': region_JSON,
            'dimensions': [img_size, img_size],        # Exact tile size (no distortion)
            'crs': 'EPSG:3857',                         # Coordinate Reference System (meters)
            'format': 'GEO_TIFF',
            'filePerBand': False
        })

        try:
            r = requests.get(url)
            r.raise_for_status()  # Raises HTTPError if the request returned an unsuccessful status code
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"Saved at: {filepath}")
        except requests.RequestException as e:
            print(f"Failed to download image at {filepath}. Error: {e}")
            print(f"URL was: {url}")

    def downloadMonthlyComposite(
        self, 
        ROI_grid_gdf: gpd.GeoDataFrame, 
        startDate: str, 
        endDate: str, 
        filename: str
    ) -> None:
        """
        Downloads a median composite image for each tile in a uniform ROI grid, clipped by each tile geometry.

        For each grid cell in the ROI, the method clips the composite to that tile and downloads the image
        if the tile contains sufficient valid data pixels.

        Args:
            ROI_grid_gdf (gpd.GeoDataFrame):
                A GeoDataFrame representing the ROI divided into uniform grid tiles.
            startDate (str):
                Start date for the image collection filter, formatted as 'YYYY-MM-DD'.
            endDate (str):
                End date for the image collection filter, formatted as 'YYYY-MM-DD'.
            filename (str):
                The filename to use when saving each tile's downloaded GeoTIFF image.

        Returns:
            None
        """
        composite = self.load_ee_composite(ROI_grid_gdf, startDate, endDate)

        if composite:
            ROI_grid_gdf = ROI_grid_gdf.to_crs(epsg=3857)  # Matches grid CRS and download projection

            for i, cell in ROI_grid_gdf.iterrows():
                tile_geom = cell.geometry
                region_JSON = shapely.geometry.mapping(tile_geom)
                tile_geom_ee = ee.Geometry(region_JSON, 'EPSG:3857')  # Explicitly tell EE it's 3857
                tile_image = composite.clip(tile_geom_ee)

                if self.checkTileValidity(tile_image=tile_image, tile_geom_ee=tile_geom_ee):
                    print(f"Downloading Tile {i}...")
                    filepath = os.path.join(self.datasetDir, f"tile_{i}")
                    os.makedirs(filepath, exist_ok=True)
                    self.downloadURL(tile_image, filepath=os.path.join(filepath, filename))  # Pass clipped image only
                else:
                    print(f"Skipped Tile {i}: Most pixels masked or invalid")

    def startDownload(
        self, 
        roi_path: str, 
        startYear: int, 
        endYear: int
    ) -> bool:
        """
        Starts the bulk image download process over a specified ROI and date range.

        For each month between `startYear` and `endYear`, the method:
        - Generates a grid over the ROI.
        - Validates year range.
        - Submits monthly composite download jobs in parallel using ThreadPoolExecutor.

        Args:
            roi_path (str): 
                Path to the shapefile containing the region of interest (ROI).
            startYear (int): 
                Starting year for the download (inclusive).
            endYear (int): 
                Ending year for the download (inclusive).

        Returns:
            bool:
                True if download tasks were submitted successfully; False if an error occurred.
        """
        # Load ROI shapefile
        ROI_gdf = gpd.read_file(roi_path)

        # Generate grid patches over the ROI
        ROI_grid_gdf = patch_roi(
            roi=ROI_gdf, 
            tile_size_px=self.img_size, 
            res_m=self.res_m
        )

        # Validate the year range
        try:
            checkDateRange(startYear, endYear)
        except Exception as e:
            print(f"Error Downloading...\n{e}")
            return False

        years = list(range(startYear, endYear + 1))
        months = list(range(1, 13))  # January to December

        # Download composites in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for year in years:
                for month in months:
                    max_days = calendar.monthrange(year, month)[1]
                    start_date = f"{year}-{month:02d}-01"
                    end_date = f"{year}-{month:02d}-{max_days:02d}"
                    filename = f"{year}-{month:02d}.tif"

                    future = executor.submit(
                        self.downloadMonthlyComposite, 
                        ROI_grid_gdf, 
                        start_date, 
                        end_date, 
                        filename
                    )
                    futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

        return True
    