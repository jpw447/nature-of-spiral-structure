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

full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\\ngc4995b.fits")
# log_image= np.exp(-np.log(full_image)/np.log(100))
log_image = np.log10(full_image)

count, intensity, _ = plt.hist(log_image.flatten(), bins='auto')
# plt.close()
largest_intensity = np.max(count)
max_brightness = intensity[np.where(count == largest_intensity)][0]

fig = plt.figure()
ax = fig.gca()
full_im = ax.imshow(log_image, cmap='gray', vmin=max_brightness, vmax=2.38)
ax.set_title("IC 4444 (rescaled)")
plt.grid(False)
plt.show()