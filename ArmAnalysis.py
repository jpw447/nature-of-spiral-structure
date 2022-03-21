import numpy as np
import matplotlib.pyplot as plt
import cv2
from astropy.io import fits

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

def crop(image):
    '''
    This function crops the deproejcted image removing any black space.
    Please delete if its usage is not needed.
    '''
    y_nonzero, x_nonzero = np.nonzero(image)
    return image[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]

def deprojection(image):
    '''
    This function deprojects the image using suitable input from the user.
    '''
    try:
        v_strch = float(input("Vertical stretch amount: "))
    except:
        v_strch = 1.0
    try:
        h_strch = float(input("Horizontal stretch amount: "))
    except:
        h_strch = 1.0

    img = image.data
    u_img = np.array(img)
    resized_image = cv2.resize(u_img, (round(np.shape(u_img)[1]*h_strch), round(np.shape(u_img)[0]*v_strch))) 
    resized_image = crop(resized_image)

    #This plots a circle for help with stretching (408 and 208 should be replaces with centre)
    #cv2.circle(resized_image,(round(408*h_strch), round(208*v_strch)), 150, (0,255,0), 2)

    return resized_image


def image_display(path, save_path, galaxy_name, colour_band):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Plots using plt.imshow from matplotlib
    '''
    '''
    This first name-grabbing section will later need updating to filtering through
    a list of filenames provided to it for each colour band
    ''' 
    
    # name = input("Type the galaxy name in the correct file format: ")
    name = galaxy_name
    print("NAME IS "+name)
    print("SEARCHING FOR ->>> "+str(path)+"\\{}.fits".format(name))
    full_image = fits.getdata(str(path)+"\\{}.fits".format(name))    
    log_image = np.log10(full_image)
    flattened_log = log_image.flatten()
    flattened_log = np.where(abs(flattened_log) == np.inf, np.nan, flattened_log)
    
    # Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
    fig_hist = plt.figure()
    ax_hist = fig_hist.gca()
    pixel_count, pixel_intensity, _ = plt.hist(flattened_log, bins='auto')
    ax_hist.set_title("Image Histogram")
    plt.close()
    
    percentage = 0.005
    vmin, vmax = histogram_limiter(percentage, pixel_count, pixel_intensity)
    
    # The image with a calculated, restricted brightness range
    fig_image = plt.figure(figsize=(10,10))
    ax_image = fig_image.gca()
    
    # Replaces log_image with deprojected image
    depro_image = deprojection(log_image)
    ax_image.imshow(depro_image, cmap='gray', vmin=vmin, vmax=vmax)
    
    ax_image.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False) 
    ax_image.set_title("{} in {}-Band".format(galaxy_name, colour_band), fontsize=24)
    plt.grid(False)
    plt.savefig(save_path+"\\{}{}.jpg".format(name,colour_band))
    
    input("Press enter to continue...")
