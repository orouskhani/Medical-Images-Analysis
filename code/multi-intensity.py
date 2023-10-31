import numpy as np
import os
import nibabel as nib
from scipy import ndimage








dir_path = os.path.dirname("/home/labels/")
print(dir_path)



def calculate_aneurysm_intensity(image_file, mask_file):
    # Load the image file and mask file
    image_data = nib.load(image_file).get_fdata()
    mask_data = nib.load(mask_file).get_fdata()

    # Perform connected component analysis to separate aneurysms
    labeled_mask, num_labels = ndimage.label(mask_data==1)

    # Initialize a list to store the intensities of individual aneurysms
    mean_intensities = []
    var_intensities = []

    # Initialize an empty array to store the ROI data
    roi_data = np.zeros_like(image_data)

    # Iterate through each labeled region
    for label in range(1, num_labels + 1):
        # Create a binary mask for the current aneurysm
        aneurysm_mask = np.where(labeled_mask == label, 1, 0)
        # Apply the aneurysm mask to the image
        roi_data = image_data * aneurysm_mask
        roi_data = roi_data[aneurysm_mask==1]
        roi_data = (np.abs(roi_data-roi_data.min())) / (roi_data.max() - roi_data.min())
        
        #print("roi_Min is: ", roi_data.min())
        #print("roi_max is", roi_data.max())
        
        # Calculate the intensity of the ROI
        roi_intensity_mean = np.mean(roi_data)  # Example: mean intensity calculation
        roi_intensity_var = np.var(roi_data)  # Example: mean intensity calculation
        #print("roi_intensity_mean is: ",roi_intensity_mean)
        #print("roi_intensity_var is: ",roi_intensity_var)
       
        # Append the intensity to the list
        mean_intensities.append(roi_intensity_mean)
        var_intensities.append(roi_intensity_var)
        


        
    return mean_intensities, var_intensities


# loop through all files in the directory
for data in os.listdir(dir_path):

    if "_0000.nii.gz" in data:
        mask = data.replace("_0000","")
        print(mask)
        Intensity_mean , Intensity_var = calculate_aneurysm_intensity(data,mask)
        print(Intensity_mean,Intensity_var)



