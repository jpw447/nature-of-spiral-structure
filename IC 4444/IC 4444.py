from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

# Creating a list of colours to loop through, then importing each FITS file into
# Python. The data is then retrieved and stored in image_concat, before being
# sumperimposed onto each other to form the full_image
full_image = fits.getdata("ic4444b.fits")

# Establishing an arbirarily chosen intensity threshold  to create two images
# one of the spiral arms and the other of the central bulge

lower_arm_threshold = 0.4
upper_arm_threshold = 0.6

plt.figure()
histogram = plt.hist(full_image.ravel(), bins=100)

plt.figure()
plt.imshow(full_image, cmap='gray', vmin=20, vmax = 75)
plt.title("IC 4444")
plt.colorbar()
plt.grid(None)
plt.show()