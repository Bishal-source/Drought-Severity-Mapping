"""
Load Study Area and NDVI Dataset
--------------------------------
This module loads the Rajasthan boundary and the
scaled MODIS NDVI ImageCollection.
"""

import ee

from gee.config import (
    PROJECT_ID,
    STATE_NAME,
    NDVI_DATASET,
    START_DATE,
    END_DATE,
)

# ---------------------------------
# Initialize Earth Engine
# ---------------------------------
ee.Initialize(project=PROJECT_ID)


def load_ndvi():
    """
    Load Rajasthan boundary and scaled MODIS NDVI.

    Returns
    -------
    tuple
        (rajasthan, ndvi_collection)
    """

    # ---------------------------------
    # Load State Boundary
    # ---------------------------------
    states = ee.FeatureCollection("FAO/GAUL/2015/level1")

    rajasthan = states.filter(
        ee.Filter.eq("ADM1_NAME", STATE_NAME)
    )

    # ---------------------------------
    # Load MODIS NDVI
    # ---------------------------------
    ndvi = (
        ee.ImageCollection(NDVI_DATASET)
        .filterDate(START_DATE, END_DATE)
        .filterBounds(rajasthan)
        .select("NDVI")
    )

    # ---------------------------------
    # Apply MODIS Scale Factor
    # ---------------------------------
    def scale_ndvi(image):
        return (
            image.multiply(0.0001)
            .copyProperties(image, image.propertyNames())
        )

    ndvi = ndvi.map(scale_ndvi)

    return rajasthan, ndvi


if __name__ == "__main__":

    rajasthan, ndvi = load_ndvi()

    print("=" * 50)
    print("Study Area :", STATE_NAME)
    print("Dataset    :", NDVI_DATASET)
    print("Images     :", ndvi.size().getInfo())
    print("Band       :", ndvi.first().bandNames().getInfo())
    print("=" * 50)