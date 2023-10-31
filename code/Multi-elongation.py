import numpy as np
import nibabel as nib
import cv2
import os
from skimage.measure import label, regionprops
from skimage.draw import ellipse
import numpy as np
from scipy import ndimage




dir_path = os.path.dirname("/home/labelsTs/")

def calculate_aneurysm_elongation(mask_file):
            # Load the mask file
            mask_data = nib.load(mask_file).get_fdata()

            # Perform connected component analysis to separate aneurysms
            labeled_mask, num_labels = ndimage.label(mask_data==1)

            # Initialize a list to store the sizes of individual aneurysms
            aneurysm_elongations = []

            # Iterate through each labeled region
            for label in range(1, num_labels + 1):
                # Create a binary mask for the current aneurysm
                aneurysm_mask = np.where(labeled_mask == label, 1, 0)
                
                # Fit an ellipse to the aneurysm region
                rows, cols = np.nonzero(aneurysm_mask)[:2]
                ellipse_params = cv2.fitEllipse(np.column_stack((cols, rows)))

                # Extract major and minor axis lengths from the ellipse parameters
                major_axis = max(ellipse_params[1])
                minor_axis = min(ellipse_params[1])

                # so elongation rate: the higher, the less irregularity, so elongation_rate = 1 is the prefect circle
                elongation_rate = minor_axis / major_axis

                # Append the size to the list
                aneurysm_elongations.append(elongation_rate)

            return aneurysm_elongations


# loop through all files in the directory
for file_name in os.listdir(dir_path):

    if "nii.gz" in file_name:
        print(file_name)
        aneurysm_elongations = calculate_aneurysm_elongation(file_name)
        print(aneurysm_elongations)








