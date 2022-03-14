from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
import cv2
plt.style.use(astropy_mpl_style)

# Loads the image and rescales the data using base 10 logarithms
full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\\ngc5054b.fits")
log_image = np.log10(full_image)

# Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
fig_hist = plt.figure()
ax_hist = fig_hist.gca()
count, intensity, _ = plt.hist(log_image.flatten(), bins='auto')
ax_hist.set_title("Image Histogram")

# Maximum brightness in the image
max_brightness = intensity[np.argmax(count)]
max_count = np.max(intensity)
ax_hist.set_xlim(0, max_count)

# Grabbing the top (threshold*100)% most bright pixels
threshold = 0.9
bright_image = np.where(log_image > threshold*max_brightness, log_image, 0)

# Histogram of bright image
fig_bright_hist = plt.figure()
ax_bright_hist = fig_bright_hist.gca()
bright_hist = plt.hist(bright_image.flatten(), bins='auto')
ax_bright_hist.set_title("Bright Image Histogram")
ax_bright_hist.set_xlim(0, max_count)

# The bright image above the specified threshold
fig_bright_image = plt.figure()
ax_bright_image = fig_bright_image.gca()
bright_im = ax_bright_image.imshow(bright_image, cmap='gray', vmin=max_brightness, vmax=2.6)
ax_bright_image.set_title("NGC 4995 (above "+str(threshold*100)+"% intensity)")
plt.grid(False)
plt.show()