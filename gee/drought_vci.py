"""
Vegetation Condition Index (VCI)
--------------------------------
This module calculates the Vegetation Condition Index
using the scaled MODIS NDVI ImageCollection.
"""

import ee

from gee.config import PROJECT_ID
from gee.load_data import load_ndvi

# ---------------------------------
# Initialize Earth Engine
# ---------------------------------
ee.Initialize(project=PROJECT_ID)


def calculate_vci():
    """
    Calculate Vegetation Condition Index (VCI).

    Returns
    -------
    tuple
        (rajasthan, vci_image)
    """

    # Load study area and NDVI
    rajasthan, ndvi = load_ndvi()

    # NDVI statistics
    ndvi_min = ndvi.min()
    ndvi_max = ndvi.max()
    ndvi_mean = ndvi.mean()

    # Prevent division by zero
    denominator = ndvi_max.subtract(ndvi_min)

    vci = (
        ndvi_mean
        .subtract(ndvi_min)
        .divide(denominator.max(0.0001))
        .multiply(100)
        .rename("VCI")
    )

    return rajasthan, vci


if __name__ == "__main__":

    _, vci = calculate_vci()

    print("=" * 50)
    print("VCI calculated successfully.")
    print("Band:", vci.bandNames().getInfo())
    print("=" * 50)