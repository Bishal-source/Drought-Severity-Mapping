import os

import ee
import pandas as pd
import matplotlib.pyplot as plt

from gee.config import SCALE, VCI_CLASSES
from gee.classify_drought import classify_drought


# =====================================================
# Create Output Directories
# =====================================================

os.makedirs("results/csv", exist_ok=True)
os.makedirs("results/figures", exist_ok=True)


# =====================================================
# Load Classified Drought Map
# =====================================================

rajasthan, drought = classify_drought()


# =====================================================
# Create Area Image
# =====================================================

area_image = (
    ee.Image.pixelArea()
    .divide(1e6)
    .rename("area")
    .addBands(drought.rename("class"))
)


# =====================================================
# Calculate Area for All Classes (Single Request)
# =====================================================

result = area_image.reduceRegion(
    reducer=ee.Reducer.sum().group(
        groupField=1,
        groupName="class"
    ),
    geometry=rajasthan.geometry(),
    scale=SCALE,
    maxPixels=1e13
).getInfo()


groups = result["groups"]


# =====================================================
# Convert to Dictionary
# =====================================================

area_dict = {}

total_area = 0

for item in groups:
    class_id = int(item["class"])
    area = item["sum"]

    area_dict[class_id] = area
    total_area += area


# =====================================================
# Create DataFrame
# =====================================================

statistics = []

for class_id, class_name in VCI_CLASSES.items():

    area = area_dict.get(class_id, 0)

    percentage = (area / total_area) * 100 if total_area > 0 else 0

    statistics.append({
        "Class": class_name,
        "Area (km²)": round(area, 2),
        "Percentage (%)": round(percentage, 2)
    })


df = pd.DataFrame(statistics)


# =====================================================
# Print Statistics
# =====================================================

print("\n")
print("=" * 60)
print("DROUGHT AREA STATISTICS")
print("=" * 60)
print(df)
print("=" * 60)


# =====================================================
# Export CSV
# =====================================================

csv_path = "results/csv/drought_area_statistics.csv"

df.to_csv(csv_path, index=False)

print(f"\nCSV saved to: {csv_path}")


# =====================================================
# Bar Chart
# =====================================================

plt.figure(figsize=(10, 6))

colors = [
    "#8B0000",
    "#FF4500",
    "#FFD700",
    "#ADFF2F",
    "#006400"
]

plt.bar(
    df["Class"],
    df["Area (km²)"],
    color=colors
)

plt.title("Area under Different Drought Severity Classes")

plt.xlabel("Drought Class")

plt.ylabel("Area (km²)")

plt.xticks(rotation=20)

plt.tight_layout()

bar_path = "results/figures/drought_area_bar_chart.png"

plt.savefig(bar_path, dpi=300)

plt.close()

print(f"Bar chart saved to: {bar_path}")


# =====================================================
# Pie Chart
# =====================================================

plt.figure(figsize=(8, 8))

plt.pie(
    df["Area (km²)"],
    labels=df["Class"],
    autopct="%1.1f%%",
    startangle=90,
    colors=colors
)

plt.title("Distribution of Drought Severity")

plt.tight_layout()

pie_path = "results/figures/drought_area_pie_chart.png"

plt.savefig(pie_path, dpi=300)

plt.close()

print(f"Pie chart saved to: {pie_path}")


# =====================================================
# Finished
# =====================================================

print("\nArea statistics completed successfully.")