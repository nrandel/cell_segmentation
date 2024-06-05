# %%
#conda activate clemclam
#https://scikit-image.org/docs/stable/api/skimage.io.html#skimage.io.imread
#https://colab.research.google.com/github/HenriquesLab/ZeroCostDL4Mic/blob/master/Colab_notebooks/StarDist_3D_ZeroCostDL4Mic.ipynb
#https://www.youtube.com/watch?v=3yk9sBja7YI&ab_channel=DigitalSreeni

# %%# 
# run interactively: python -i main.py
import numpy as np
import napari as nap
import skimage.io as io
import os

# %%# Load your source data
source_dir = "/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis"
file_path = f"{source_dir}/output/groundtruth/sample/Pd_3dpf_D3-1_L1.tif"
labels_filename = f"{source_dir}/output/groundtruth/label/labelled_Pd_3dpf_D3-1_L1.tif"
raw_data = io.imread(file_path)
source_image = raw_data[:,1,:,:] # take second channel

# %%# 
# Initialise labels
labels = np.zeros(source_image.shape, dtype=np.uint16)

#%%
#Load labels from previously saved
from skimage.io import imread
labels = imread(labels_filename)
# %%# 
# Show in Napari
v = nap.Viewer()
#v.add_image(source_image, scale=[10,1,1], contrast_limits=[0, 5000])
v.add_image(source_image, contrast_limits=[0,30000])
v.add_labels(labels)


#v.display()

# %%# 
# Save
io.imsave(labels_filename, labels)

#%%
# To save with safeguard 
# Not Working#
#labels_certain = v.layers[1].data
#assert np.all(labels_certain == labels)==True
#if os.path.exists(labels_filename):
#    i = input("You are about to overwrite an image! Are you sure? Please 'y' to save")
#    if i=="y":
#        io.imsave(labels_filename, labels)

# %%

import numpy as np
import skimage.io
from skimage.measure import regionprops
segs = skimage.io.imread("/Users/nadine/Documents/paper/Naomi-NS-maturation/cLM_EdU-larvae/analysis/output/groundtruth/label/labelled_Pd_3dpf_D3-1_L1.tif")
regions = regionprops(segs)
centroids = np.array([r.centroid for r in regions])
print(centroids.shape)

# %%
