from osgeo import gdal
from PIL import Image
import os
import numpy as np

def nitf_to_png(ntf_file_path, image_name, max_size=500):
    # Use GDAL to read the NITF file
    ntf_dataset = gdal.Open(ntf_file_path)

    # Get the number of bands in the NITF file
    num_bands = ntf_dataset.RasterCount

    # If the image has multiple bands, we need to handle each band separately
    if num_bands > 1:
        # Create an empty list to store each band's data
        bands_data = []

        # Only take the first three bands (assuming RGB)
        num_bands_to_use = min(3, num_bands)

        # Read each band's data and append it to the list
        for b in range(num_bands_to_use):
            band = ntf_dataset.GetRasterBand(b + 1)  # GDAL uses 1-based index
            bands_data.append(band.ReadAsArray())

        # Stack the bands data along the third axis (color channels)
        ntf_image = np.dstack(bands_data)
    else:
        # If there's only one band, we can read it directly
        ntf_image = ntf_dataset.ReadAsArray()

    # Normalize the image data to be in the range (0-255)
    ntf_image = ((ntf_image - ntf_image.min()) / (ntf_image.max() - ntf_image.min()) * 255).astype(np.uint8)

    # Convert the NITF image data to a format that PIL can handle
    image_data = Image.fromarray(ntf_image)

    # Save the resized image as PNG
    png_file_path = os.path.join(os.path.dirname(ntf_file_path), f"{os.path.splitext(image_name)[0]}.png")
    image_data.save(png_file_path)

    return png_file_path
