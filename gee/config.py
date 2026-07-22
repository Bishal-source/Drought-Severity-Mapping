"""
Project Configuration
---------------------
This file contains all configurable parameters for the
Drought Severity Mapping project.
"""

# ---------------------------------
# Google Earth Engine Project
# ---------------------------------
PROJECT_ID = "spherical-park-503216-d1"

# ---------------------------------
# Study Area
# ---------------------------------
STATE_NAME = "Rajasthan"

# ---------------------------------
# Dataset
# ---------------------------------
NDVI_DATASET = "MODIS/061/MOD13Q1"

# ---------------------------------
# Study Period
# ---------------------------------
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"

# ---------------------------------
# Spatial Resolution (meters)
# ---------------------------------
SCALE = 250

# ---------------------------------
# VCI Classification
# ---------------------------------
VCI_CLASSES = {
    1: "Extreme Drought",
    2: "Severe Drought",
    3: "Moderate Drought",
    4: "Mild Drought",
    5: "No Drought"
}

# ---------------------------------
# Color Palette
# ---------------------------------
VCI_PALETTE = [
    "#8B0000",   # Extreme
    "#FF4500",   # Severe
    "#FFD700",   # Moderate
    "#ADFF2F",   # Mild
    "#006400"    # No Drought
]