'''
This file is used for analysing the OSU images in the OSU file.
The files are not kept in the Github repository but are stored locally,
and are available via Sharepoint download.
'''

from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import widgets
plt.style.use(astropy_mpl_style)

def max_brightness_change(val):
    plt.clear()

full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\ic4444b.fits")
log_image= np.log10(full_image)

histogram_log = plt.hist(log_image.ravel(), bins='auto')
plt.close()
largest_intensity = np.max(histogram_log[0])
max_brightness = histogram_log[1][np.where(histogram_log[0] == largest_intensity)]


fig = plt.figure()
ax = fig.gca()
full_im = ax.imshow(log_image, cmap='gray', vmin=max_brightness, vmax=2.5)
max_sax = plt.axes([0.1, 0.1, 0.8, 0.05]) 
max_slider = widgets.Slider(max_sax, 'Max Brightness', 0, 3*max_brightness)
max_slider.on_changed(max_brightness_change)
ax.set_title("IC 4444 (rescaled)")
plt.grid(False)
plt.show()