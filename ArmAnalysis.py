import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False)

def histogram_limiter(percentage, count, intensity):
    '''
    Finds the maximum brightness in the histogram, max_brightness.
    intensity = x-values
    count = y-values
    Works by finding the histogram indices where the brightness exceeds the 
    specified threshold. The edge idices are then returned to give an
    appropriate brightness range for image display.
    '''
    threshold = percentage*np.max(count)
    bright_indices = np.where(count > threshold)[0]
    lower_bound, upper_bound = bright_indices[0], bright_indices[-1]
    vmin, vmax = intensity[lower_bound], intensity[upper_bound]
    
    return vmin, vmax

def image_display(path, galaxy_name, colour_band):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Plots using plt.imshow from matplotlib
    '''
    '''
    This first name-grabbing section will later need updating to filtering through
    a list of filenames provided to it for each colour band
    '''
    name = input("Type the galaxy name in the correct file format: ")
    
    try:
        full_image = fits.getdata(str(path)+"\\{}.fits".format(name))
    except FileNotFoundError:
        print("ERROR: File not found. Check the path provided and ensure it doesn't end in '\\\\', and\
              that you've provided the correct file name.")
        return
    
    log_image = np.log10(full_image)
    
    # Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
    fig_hist = plt.figure()
    ax_hist = fig_hist.gca()
    pixel_count, pixel_intensity, _ = plt.hist(log_image.flatten(), bins='auto')
    ax_hist.set_title("Image Histogram")
    
    percentage = 0.005
    vmin, vmax = histogram_limiter(percentage, pixel_count, pixel_intensity)
    
    # The image with a calculated, restricted brightness range
    fig_image = plt.figure()
    ax_image = fig_image.gca()
    ax_image.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
    ax_image.set_title("{} in {}-Band".format(galaxy_name, colour_band))
    plt.grid(False)
    plt.show()

