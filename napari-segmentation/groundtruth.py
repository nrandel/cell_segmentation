#%%
import numpy as np
import tifffile as tiff
import os

#%%
# Load the TIFF file
tiff_file_path = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/label/labelled_Pd_3dpf_D3-1_L1.tif'
image_3d = tiff.imread(tiff_file_path)
print(f"Loaded image shape: {image_3d.shape}")

#%%
# Parameters
block_size = (40, 800, 800) #16, 32, 32
overlap_percentage = 0.30

#%%
# Calculate the overlap in pixels
overlap = [int(dim * overlap_percentage) for dim in block_size]

# Calculate the step size
step = [block_size[i] - overlap[i] for i in range(3)]

def chop_image(image, block_size, step):
    x_size, y_size, z_size = image.shape
    x_step, y_step, z_step = step
    blocks = []

    for x in range(0, x_size - block_size[0] + 1, x_step):
        for y in range(0, y_size - block_size[1] + 1, y_step):
            for z in range(0, z_size - block_size[2] + 1, z_step):
                block = image[x:x + block_size[0], y:y + block_size[1], z:z + block_size[2]]
                blocks.append(block)

    return blocks

blocks = chop_image(image_3d, block_size, step)

#%%
# Create directory to save chopped images
output_dir = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/choped-label'
os.makedirs(output_dir, exist_ok=True)

# Save each block as a separate TIFF file
for i, block in enumerate(blocks):
    output_path = os.path.join(output_dir, f'block_{i}.tif')
    tiff.imwrite(output_path, block)

# %%

# Directory containing the chopped images
output_dir = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/choped-label'

# Iterate through the TIFF files in the directory
for filename in os.listdir(output_dir):
    if filename.endswith('.tif'):
        file_path = os.path.join(output_dir, filename)
        # Load the TIFF file
        image = tiff.imread(file_path)
        # Check if the sum of pixel values is 0
        if np.sum(image) == 0:
            # Remove the file
            os.remove(file_path)
            print(f"Removed {filename} with sum of pixel values = 0")

# %%
