#%%
import numpy as np
import tifffile as tiff
import os

#%%
# Load the raw image and the mask image
raw_image_path = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/sample/C2-Pd_3dpf_D3-1_L1.tif'
mask_image_path = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/label/labelled_Pd_3dpf_D3-1_L1.tif'
raw_image = tiff.imread(raw_image_path)
mask_image = tiff.imread(mask_image_path)

print("Raw image shape:", raw_image.shape)
print("Mask image shape:", mask_image.shape)

#%%
# Parameters (adjusted to the z, y, x order)
block_size = (40, 160, 160)  # z, y, x
overlap_percentage = 0.30

#%%
# Calculate the overlap in pixels
overlap = [int(dim * overlap_percentage) for dim in block_size]

#%%
# Calculate the step size
step = [block_size[i] - overlap[i] for i in range(3)]

def chop_images(raw_image, mask_image, block_size, step):
    z_size, y_size, x_size = raw_image.shape
    z_step, y_step, x_step = step
    raw_blocks = []
    mask_blocks = []
    coordinates = []

    for z in range(0, z_size - block_size[0] + 1, z_step):
        for y in range(0, y_size - block_size[1] + 1, y_step):
            for x in range(0, x_size - block_size[2] + 1, x_step):
                raw_block = raw_image[z:z + block_size[0], y:y + block_size[1], x:x + block_size[2]]
                mask_block = mask_image[z:z + block_size[0], y:y + block_size[1], x:x + block_size[2]]
                raw_blocks.append(raw_block)
                mask_blocks.append(mask_block)
                coordinates.append((z, y, x))

    return raw_blocks, mask_blocks, coordinates

raw_blocks, mask_blocks, coordinates = chop_images(raw_image, mask_image, block_size, step)
print(f"Total blocks created: {len(raw_blocks)}")

#%%
# Create directory to save chopped images
output_dir = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/chopped_images'
os.makedirs(output_dir, exist_ok=True)
print(f"Saving blocks to directory: {output_dir}")

# Save each block as a separate TIFF file
for i, (raw_block, mask_block, coord) in enumerate(zip(raw_blocks, mask_blocks, coordinates)):
    raw_output_path = os.path.join(output_dir, f'raw_{i}_z{coord[0]}_y{coord[1]}_x{coord[2]}.tif')
    mask_output_path = os.path.join(output_dir, f'mask_{i}_z{coord[0]}_y{coord[1]}_x{coord[2]}.tif')
    tiff.imwrite(raw_output_path, raw_block)
    tiff.imwrite(mask_output_path, mask_block)
    print(f"Saved raw block {i} and mask block {i} at coordinates {coord}")

# %%
# Directory containing the chopped images
chopped_images_dir = '/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/chopped_images'

# Iterate through the files in the directory
for filename in os.listdir(chopped_images_dir):
    if filename.startswith('mask_') and filename.endswith('.tif'):
        mask_file = os.path.join(chopped_images_dir, filename)
        raw_file = os.path.join(chopped_images_dir, 'raw_' + filename[5:])  # Get corresponding raw image file

        # Load the mask image and check sum of pixel values
        mask_image = tiff.imread(mask_file)
        if np.sum(mask_image) == 0:
            # Delete both the mask and raw image files
            os.remove(mask_file)
            os.remove(raw_file)
            print(f"Deleted {mask_file} and {raw_file} due to sum of pixel values = 0")

# %%
