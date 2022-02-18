from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

colours = ['g', 'r', 'i', 'u', 'z']
image_list = [fits.open("frame-{}-004264-4-0259.fits".format(colour)) for colour in colours]
image_concat = [image[0].data for image in image_list]

full_image = np.sum(image_concat, axis=0)

# plt.figure()
# histogram = plt.hist(full_image.ravel(), bins=1000)
plt.figure()
plt.imshow(full_image, cmap='gray', vmin=10, vmax=50)
plt.grid(None)
plt.show()