from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

# Loads the image and rescales the data using base 10 logarithms
full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\\ngc4995b.fits")
log_image = np.log10(full_image)

# Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
count, intensity, _ = plt.hist(log_image.flatten(), bins='auto')
# plt.close()
largest_intensity = np.max(count)
max_brightness = intensity[np.where(count == largest_intensity)][0]

# Displaying the image
fig = plt.figure()
ax = fig.gca()
full_im = ax.imshow(log_image, cmap='gray', vmin=max_brightness, vmax=2.6)
ax.set_title("NGC 4995 (rescaled)")
plt.grid(False)
plt.show()