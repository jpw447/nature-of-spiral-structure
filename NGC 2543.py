from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

image_file = fits.open("frame-u-003918-3-0213.fits")
image_file.info()
data = image_file[0].data

plt.figure()
plt.imshow(data)
plt.show()