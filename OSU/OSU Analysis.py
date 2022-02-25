'''
This file is used for analysing the OSU images in the OSU file.
The files are not kept in the Github repository but are stored locally,
and are available via Sharepoint download.
'''

from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
plt.style.use(astropy_mpl_style)

def update_min(val):
    full_im = ax.imshow(log_image, cmap='gray', vmin=val, vmax=2.5)
    ax.canvas.draw_idle()

full_image = fits.getdata("OSU\data\survey\ByFilter\B_band\ic4444b.fits")
log_image= np.log10(full_image)

count, intensity, _ = plt.hist(log_image.ravel(), bins='auto')
plt.close()
largest_intensity = np.max(count)
min_brightness = intensity[np.where(count == largest_intensity)][0]
max_brightness = 2.5

fig = plt.figure()
ax = fig.gca()
full_im = ax.imshow(log_image, cmap='gray', vmin=min_brightness, vmax=max_brightness)
ax_min_slider = plt.axes([0.20, 0.01, 0.65, 0.03])
min_slider = Slider(ax_min_slider, 'min', 1, 3*min_brightness, valinit=min_brightness)


min_slider.on_changed(update_min)

ax.set_title("IC 4444 (rescaled)")
plt.grid(False)
plt.show()