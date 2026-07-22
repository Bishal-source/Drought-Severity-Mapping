"""
Drought Classification
----------------------
This module classifies the Vegetation Condition Index (VCI)
into five drought severity classes.
"""

import ee

from gee.config import (
    PROJECT_ID,
    VCI_CLASSES,
)
from gee.drought_vci import calculate_vci

# ---------------------------------
# Initialize Earth Engine
# ---------------------------------
ee.Initialize(project=PROJECT_ID)


def classify_drought():
    """
    Classify VCI into drought severity classes.

    Returns
    -------
    tuple
        (rajasthan, drought_class_image)
    """

    rajasthan, vci = calculate_vci()

    drought = (
        ee.Image(0)
        .where(vci.lte(20), 1)
        .where(vci.gt(20).And(vci.lte(40)), 2)
        .where(vci.gt(40).And(vci.lte(60)), 3)
        .where(vci.gt(60).And(vci.lte(80)), 4)
        .where(vci.gt(80), 5)
        .rename("Drought_Class")
    )

    return rajasthan, drought


if __name__ == "__main__":

    _, drought = classify_drought()

    print("=" * 50)
    print("Drought Classification Completed")
    print("Band :", drought.bandNames().getInfo())

    print("\nClass Legend")
    for key, value in VCI_CLASSES.items():
        print(f"{key} : {value}")

    print("=" * 50)