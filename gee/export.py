import ee

from gee.config import PROJECT_ID
from gee.drought_vci import calculate_vci
from gee.classify_drought import classify_drought


def export_vci():

    print("\nStarting VCI export...")

    rajasthan, vci = calculate_vci()

    task = ee.batch.Export.image.toDrive(
        image=vci.clip(rajasthan),
        description="VCI_Rajasthan",
        folder="GEE_Exports",
        fileNamePrefix="VCI_Rajasthan",
        region=rajasthan.geometry(),
        scale=250,
        maxPixels=1e13,
        fileFormat="GeoTIFF"
    )

    task.start()

    print("VCI export started successfully.")
    print("Task ID:", task.id)


def export_drought():

    print("\nStarting Drought Severity export...")

    rajasthan, drought = classify_drought()

    task = ee.batch.Export.image.toDrive(
        image=drought.clip(rajasthan),
        description="Drought_Severity_Rajasthan",
        folder="GEE_Exports",
        fileNamePrefix="Drought_Severity_Rajasthan",
        region=rajasthan.geometry(),
        scale=250,
        maxPixels=1e13,
        fileFormat="GeoTIFF"
    )

    task.start()

    print("Drought Severity export started successfully.")
    print("Task ID:", task.id)


if __name__ == "__main__":

    ee.Initialize(project=PROJECT_ID)

    export_vci()

    export_drought()

    print("\nBoth export tasks have been submitted.")
    print("Check the Earth Engine Tasks page or your Google Drive.")