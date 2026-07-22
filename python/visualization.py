"""
Visualization Module
--------------------
Creates an interactive map for:
1. Vegetation Condition Index (VCI)
2. Drought Severity
"""

import os
import webbrowser
import ee
import geemap

from gee.config import (
    PROJECT_ID,
)

from gee.drought_vci import calculate_vci
from gee.classify_drought import classify_drought

# --------------------------------------------------
# Initialize Earth Engine
# --------------------------------------------------
ee.Initialize(project=PROJECT_ID)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
rajasthan, vci = calculate_vci()
_, drought = classify_drought()

# --------------------------------------------------
# Create Map
# --------------------------------------------------
Map = geemap.Map()

Map.centerObject(rajasthan, 6)

# --------------------------------------------------
# Basemap
# --------------------------------------------------
Map.add_basemap("HYBRID")

# --------------------------------------------------
# --------------------------------------------------
# Rajasthan Boundary
# --------------------------------------------------
Map.addLayer(
    rajasthan.style(
        color="white",
        fillColor="00000000",
        width=3
    ),
    {},
    "Rajasthan Boundary"
)

# --------------------------------------------------
# VCI Layer
# --------------------------------------------------
vci_palette = [
    "#8B0000",
    "#FF4500",
    "#FFFF00",
    "#7CFC00",
    "#006400"
]

Map.addLayer(
    vci.clip(rajasthan),
    {
        "min": 0,
        "max": 100,
        "palette": vci_palette
    },
    "Vegetation Condition Index",
    False
)

# --------------------------------------------------
# Drought Layer
# --------------------------------------------------
drought_palette = [
    "#800026",
    "#BD0026",
    "#FD8D3C",
    "#FED976",
    "#31A354"
]

Map.addLayer(
    drought.clip(rajasthan),
    {
        "min": 1,
        "max": 5,
        "palette": drought_palette
    },
    "Drought Severity"
)

# --------------------------------------------------
# Legend
# --------------------------------------------------
legend = {
    "Extreme Drought (0-20)": "#800026",
    "Severe Drought (20-40)": "#BD0026",
    "Moderate Drought (40-60)": "#FD8D3C",
    "Mild Drought (60-80)": "#FED976",
    "No Drought (80-100)": "#31A354",
}

Map.add_legend(
    title="VCI Drought Classes",
    legend_dict=legend,
)


# --------------------------------------------------
# Save Map
# --------------------------------------------------
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

output_folder = os.path.join(project_root, "results", "maps")

os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, "drought_map.html")

Map.to_html(output_file)

print("=" * 60)
print("Interactive map created successfully.")
print(f"Saved to:\n{output_file}")
print("=" * 60)

# --------------------------------------------------
# Open Browser
# --------------------------------------------------
webbrowser.open("file://" + os.path.abspath(output_file))