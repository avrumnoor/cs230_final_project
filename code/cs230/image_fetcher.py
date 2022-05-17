import requests
import numpy as np
from tqdm import tqdm

# Remove API key when submitting code
api_key = "<Put API Key here>"

url = "https://maps.googleapis.com/maps/api/staticmap?"

# Choose what grid sampling method
sampling = "UAR"

grid_path = "../../data/int/grids/"

# Load 100000 samples from grid based on sampling method
grid = np.load(grid_path + f"CONTUS_16_640_{sampling}_100000_0.npz")

# Load full grid for testing
full_grid = np.load(grid_path + "grid_CONTUS_16_640.npz")

sampling_path = "CONTUS_" + sampling + "/"

output_path = "../../data/raw/imagery/" + sampling_path

# Print some values just for testing
print("Sampling mode:")
print(sampling)
print("Grid columns:")
print(grid.files)
print("Number of samples:")
assert(len(grid["ID"]) == len(grid["lat"]) == len(grid["lon"]))
print(len(grid["lat"]))
ids = grid["ID"][:10]
print("Sample ids:")
print(ids)
print("Zoom:")
zoom = grid["zoom"]
print(zoom)
print("Pixels:")
pix = grid["pixels"]
print(pix)
real_latlons = np.hstack((grid["lat"][:, np.newaxis], grid["lon"][:, np.newaxis]))
print("Sample lat+lons:")
print(real_latlons.shape)
print(real_latlons[:10])

print("Full grid columns")
print(full_grid.files)
print("# lat, # lon:")
print(len(full_grid["lat"]), len(full_grid["lon"]))
i = np.array([int(ix.split(",")[0]) for ix in ids])
j = np.array([int(ix.split(",")[1]) for ix in ids])
ij = np.vstack((i, j)).T
print("Sample ids:")
print(ij)
lats, lons = full_grid["lat"][ij[:, 0] - 1], full_grid["lon"][ij[:, 1] - 1]
print("Sample lat+lons:")
print(np.vstack((lats, lons)).T)

# Helper function to generate the end file name 
def generate_image_file_name(lat, lon, zoom, pix):
  return f"{lat}_{lon}_{zoom}_{pix}_{pix}.png"

# test function to verify file name output
def print_output_file_names(limit):
  for latlon in real_latlons[:10]:
    lat, lon = latlon[0], latlon[1]
    print(generate_image_file_name(lat, lon, 16, 640))

print_output_file_names(10)

# MODIFY AT YOUR OWN RISK PLEASE BE CAREFUL
image_start, image_end = 0, 3

# function to actually download the images
def download_images(start=0, end=0):
  # get and save the images
  for latlon in tqdm(real_latlons[image_start:image_end]):
    lat, lon = latlon[0], latlon[1]
    r = requests.get(url + f"center={lat},{lon}&zoom={16}&size={640}x{640}&maptype=satellite&key={api_key}")
    filename = output_path + generate_image_file_name(lat, lon, 16, 640)
    with open(filename, 'wb') as f:
      f.write(r.content)

# download_images(image_start, image_end)
