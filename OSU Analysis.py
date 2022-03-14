from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
import cv2
plt.style.use(astropy_mpl_style)

# Loads the image and rescales the data using base 10 logarithms
name = input("Type the galaxy name in the correct file format: ")
full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\\{}.fits".format(name))
log_image = np.log10(full_image)

# Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
fig_hist = plt.figure()
ax_hist = fig_hist.gca()
count, intensity, _ = plt.hist(log_image.flatten(), bins='auto')
ax_hist.set_title("Image Histogram")

'''
This finds the maximum brightness in the histogram, max_brightness.
max_brightness is the brightness with the most pixels
'''
# Finds the maximum brightness in the histogram, max_brightness.
# intensity = x-values
# count = y-values
percentage = 0.005
max_brightness = intensity[np.argmax(count)]                        # Brightness with most pixels
threshold = percentage*np.max(count)                                # Arbitrary threshold
bright_indices = np.where(count > threshold)[0]                     # Histogram indices where brightness exceeds threshold
lower_bound, upper_bound = bright_indices[0], bright_indices[-1]    # Min/max of above
vmin, vmax = intensity[lower_bound], intensity[upper_bound]         # Brightness range

# The bright image above the specified threshold
fig_image = plt.figure()
ax_image = fig_image.gca()
image = ax_image.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
ax_image.set_title("NGC 4995 (above "+str(threshold*100)+"% intensity)")
plt.grid(False)
plt.show()