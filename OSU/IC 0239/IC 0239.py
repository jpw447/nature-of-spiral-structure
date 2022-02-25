'''
This file is used for analysing the OSU images in the OSU file.
The files are not kept in the Github repository but are stored locally,
and are available via Sharepoint download.
'''

from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

galaxy_name = 'ic0239'

full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\{}b.fits".format(galaxy_name))
log_image= np.log10(full_image)

histogram_log = plt.hist(log_image.ravel(), bins='auto')
largest_intensity = np.max(histogram_log[0])
max_brightness = histogram_log[1][np.where(histogram_log[0] == largest_intensity)]

fig, ax = plt.subplots(1,2)
pos_im = ax[0].imshow(log_image, cmap='gray', vmin=2, vmax=5)
full_im = ax[1].imshow(log_image, cmap='gray', vmin=max_brightness, vmax=1.7)
ax[0].set_title(galaxy_name)
ax[0].grid(False)
ax[1].grid(False)
ax[1].set_title(str(galaxy_name)+" (rescaled)")
plt.show()