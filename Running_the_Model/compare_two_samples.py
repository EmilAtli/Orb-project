import geopandas as gpd
import numpy as np
import os
from scipy.ndimage import map_coordinates
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

gdf = gpd.read_file("./output.gpkg", layer="output")
npy_folder = "./inference/"

def get_precise_height(image_name, px, py):
    npy_name = "heights_" + image_name.replace(".png", ".npy")
    npy_path = os.path.join(npy_folder, npy_name)
    if not os.path.exists(npy_path): return None
    arr = np.load(npy_path)
    if 0 <= px < arr.shape[1] and 0 <= py < arr.shape[0]:
        coords = np.array([[py], [px]])
        return float(map_coordinates(arr, coords, order=1, mode='nearest')[0])
    return None

gdf["predicted_height"] = gdf.apply(
    lambda row: get_precise_height(row["image"], row["px"], row["py"]), axis=1
)

valid_gdf = gdf.dropna(subset=["predicted_height", "Height"])

filtered_gdf = valid_gdf[valid_gdf["Height"] >= 5]

if filtered_gdf.empty:
    raise ValueError("No trees with height ≥ 5 meters found.")

filtered_gdf["error"] = (filtered_gdf["predicted_height"] - filtered_gdf["Height"]).abs()
best = filtered_gdf.loc[filtered_gdf["error"].idxmin()]
worst = filtered_gdf.loc[filtered_gdf["error"].idxmax()]

def plot_prediction(row, title):
    npy_name = "heights_" + row["image"].replace(".png", ".npy")
    npy_path = os.path.join(npy_folder, npy_name)
    arr = np.load(npy_path)
    px, py = int(row["px"]), int(row["py"])

    plt.imshow(arr, cmap='viridis')
    plt.scatter([px], [py], c='red', s=60, marker='x', label='Tree Location')
    plt.text(px + 5, py, f"Pred: {row['predicted_height']:.2f}\nActual: {row['Height']:.2f}",
             color='white', fontsize=9, bbox=dict(facecolor='black', alpha=0.6))
    plt.title(f"{title} ({npy_name})")
    plt.colorbar(label='Height')
    plt.legend()
    plt.show()

    print(f"{title}\nImage: {row['image']}, Pixel: ({px}, {py})")
    print(f"Predicted: {row['predicted_height']:.2f}, Actual: {row['Height']:.2f}, Error: {row['error']:.2f}\n")

plot_prediction(best, "Most Accurate Prediction (≥ 5m Tree)")
plot_prediction(worst, "Least Accurate Prediction (≥ 5m Tree)")

