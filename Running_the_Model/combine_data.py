import geopandas as gpd
import numpy as np
import os
from scipy.ndimage import map_coordinates

input_gpkg = "./output.gpkg"
input_layer = "output"
npy_folder = "./inference/"
output_gpkg = "./output_with_predictions.gpkg"
output_layer = "predicted_output"

gdf = gpd.read_file(input_gpkg, layer=input_layer)

def get_precise_height(image_name, px, py):
    npy_name = "heights_" + image_name.replace(".png", ".npy")
    npy_path = os.path.join(npy_folder, npy_name)
    if not os.path.exists(npy_path):
        return None
    arr = np.load(npy_path)
    if 0 <= px < arr.shape[1] and 0 <= py < arr.shape[0]:
        coords = np.array([[py], [px]])
        return float(map_coordinates(arr, coords, order=1, mode='nearest')[0])
    return None

gdf["predicted_height"] = gdf.apply(
    lambda row: get_precise_height(row["image"], row["px"], row["py"]),
    axis=1
)

gdf.to_file(output_gpkg, layer=output_layer, driver="GPKG")
print("done")
