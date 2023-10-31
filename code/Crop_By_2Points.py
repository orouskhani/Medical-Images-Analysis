import itk

# Load the 3D Nifti file
input_image = itk.imread('adam_0041.nii.gz')

# Define the bounding box
point1 = [65, 0, 0]
point2 = [512, 544, 179]
min_point = [min(point1[i], point2[i]) for i in range(3)]
max_point = [max(point1[i], point2[i]) for i in range(3)]
size = [max_point[i] - min_point[i] + 1 for i in range(3)]
index = min_point

# Define the crop region
crop_region = itk.ImageRegion[3]()
crop_region.SetSize(size)
crop_region.SetIndex(index)

# Create a region of interest filter object
roi_filter = itk.RegionOfInterestImageFilter.New(input_image)
roi_filter.SetRegionOfInterest(crop_region)

# Apply the filter to the input image
cropped_image = roi_filter.GetOutput()
cropped_image.Update()

# Save the cropped image as a new Nifti file
itk.imwrite(cropped_image, 'file2.nii.gz')
