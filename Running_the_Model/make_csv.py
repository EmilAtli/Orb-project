import os
import csv

file_list = sorted(os.listdir('./output_images/'))

with open("data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["", "index", "image"]) 
    for idx, filename in enumerate(file_list):
        index = int(filename[:-4])
        writer.writerow([idx, index, filename])
