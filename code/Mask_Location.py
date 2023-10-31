import nibabel as nib
import numpy as np

# Load the NIfTI image data
img = nib.load('413.nii.gz')
data = img.get_fdata()

# Create a binary mask of the non-zero values
mask = (data != 0)

# Find the minimum and maximum x, y, and z indices of the non-zero values
nz_indices = np.argwhere(mask)
min_x, min_y, min_z = np.min(nz_indices, axis=0)
max_x, max_y, max_z = np.max(nz_indices, axis=0)

print("Minimum x index: ", min_x)
print("Maximum x index: ", max_x)
print("Minimum y index: ", min_y)
print("Maximum y index: ", max_y)
print("Minimum z index: ", min_z)
print("Maximum z index: ", max_z)
