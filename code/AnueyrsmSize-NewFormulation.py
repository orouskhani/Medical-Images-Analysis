import numpy as np
import nibabel as nib
from scipy.spatial.distance import pdist, squareform

import numpy as np
import nibabel as nib
import os
from scipy import ndimage
from scipy.spatial.distance import cdist
import math

dir_path = os.path.dirname("/data/labels/")
print(dir_path)


import nibabel as nib
import numpy as np
from scipy import ndimage

def calculate_aneurysm_size(mask_file):
    try:
        # Load the mask file
        nifti_file = nib.load(mask_file)
        voxel_size = nifti_file.header.get_zooms()

        mask_data = nifti_file.get_fdata()

        # Perform connected component analysis to separate aneurysms
        labeled_mask, num_labels = ndimage.label(mask_data == 1)

        # Initialize a list to store the volumes of individual aneurysms
        aneurysm_volumes = []

        # Iterate through each labeled region
        for label in range(1, num_labels + 1):
            # Create a binary mask for the current aneurysm
            aneurysm_mask = np.where(labeled_mask == label, 1, 0)

            # Find the coordinates of all non-zero points in the mask
            aneurysm_coordinates = np.argwhere(aneurysm_mask != 0)

            # Scale the coordinates by the voxel spacing to convert to physical units
            aneurysm_coordinates_physical = aneurysm_coordinates * voxel_size

            # Calculate pairwise distances between all points in physical units
            distances = pdist(aneurysm_coordinates_physical)

            # Create a distance matrix from pairwise distances
            distance_matrix = squareform(distances)

            # Find the indices of the two points with the maximum distance
            max_distance_indices = np.unravel_index(np.argmax(distance_matrix), distance_matrix.shape)

            # Extract the coordinates of the two farthest points in physical units
            farthest_point_1 = aneurysm_coordinates_physical[max_distance_indices[0]]
            farthest_point_2 = aneurysm_coordinates_physical[max_distance_indices[1]]

            # Calculate the Euclidean distance between the two farthest points
            max_diameter = np.linalg.norm(farthest_point_1 - farthest_point_2)

            # Print the maximum diameter in physical units
            #print(f"Maximum Diameter of Aneurysm: {max_diameter:.2f} units (e.g., millimeters)")

            # You can also save these coordinates if needed
            #print(f"Coordinates of Farthest Point 1: {farthest_point_1}")
            #print(f"Coordinates of Farthest Point 2: {farthest_point_2}")


            aneurysm_volumes.append(max_diameter)

        return aneurysm_volumes

    except Exception as e:
        print(f"Error: {str(e)}")
        return []



 

# loop through all files in the directory
for file_name in os.listdir(dir_path):

    if "nii.gz" in file_name:
        print(file_name)
        sizes = calculate_aneurysm_size(file_name)
        print(sizes)



