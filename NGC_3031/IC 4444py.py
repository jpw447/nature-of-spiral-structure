from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

# Creating a list of colours to loop through, then importing each FITS file into
# Python. The data is then retrieved and stored in image_concat, before being
# sumperimposed onto each other to form the full_image
colours = ['g', 'r', 'i', 'u', 'z']
image_list = [fits.open("NGC_3031\\frame-{}-004264-4-0259.fits".format(colour)) for colour in colours]
image_concat = [image[0].data for image in image_list]

full_image = np.sum(image_concat, axis=0)

# Establishing an arbirarily chosen intensity threshold  to create two images
# one of the spiral arms and the other of the central bulge
threshold = 5
bright_image = np.where(full_image > threshold, full_image, 0)
dim_image = np.where(full_image < threshold, full_image, 0)

lower_arm_threshold = 0.4
upper_arm_threshold = 0.6
dim_image_maximum = np.max(dim_image)

bright_spots = np.where((dim_image > lower_arm_threshold*dim_image_maximum) &
                        (dim_image < upper_arm_threshold*dim_image_maximum), dim_image, 0)

# Plots showing the bulge and spiral arms
fig_brightness, ax_brightness = plt.subplots(2,2)
ax_brightness[0,0].imshow(bright_image, cmap='gray', vmin=threshold, vmax=threshold+10)
ax_brightness[0,0].set_title("Bright Bulge Image")
ax_brightness[0,0].grid(None)
ax_brightness[0,1].imshow(dim_image, cmap='gray', vmin=0, vmax=threshold)
ax_brightness[0,1].set_title("Spiral Arms Image")
ax_brightness[0,1].grid(None)
ax_brightness[1,1].imshow(bright_spots, cmap='jet', vmin=0, vmax=threshold)
ax_brightness[1,1].set_title("Spots between "+str(lower_arm_threshold)+" and \n"
                             +str(upper_arm_threshold)+" max brightness")

fig_bands, ax_bands = plt.subplots(1,5)
for i, image in enumerate(image_concat):
    ax_bands[i].imshow(image, cmap='gray', vmin=0, vmax=5)
    ax_bands[i].grid(None)
    ax_bands[i].set_title("{}-band".format(colours[i]))

plt.figure()
plt.imshow(bright_image+dim_image, cmap='gray', vmin=0, vmax=threshold)
plt.title("NGC 3031")
plt.grid(None)
plt.show()