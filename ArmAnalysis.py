import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def image_display(axis, name, file_name, colour_min=1.7, colour_max=2.7, file_path=''):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Plots using plt.imshow from matplotlib
    '''
    full_image = fits.getdata(file_path+file_name)
    log_image = np.log10(full_image)
    axis.imshow(log_image, cmap='gray', vmin=1.5, vmax=2.7)
    axis.set_title("OSU Image of "+name)
    plt.show()
    return full_image
