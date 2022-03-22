import numpy as np
import matplotlib.pyplot as plt
import cv2
from astropy.io import fits

def histogram_limiter(percentage, count, intensity):
    '''
    Finds the maximum brightness in the histogram, max_brightness.
    Works by finding the histogram indices where the brightness exceeds the 
    specified threshold. The edge idices are then returned to give an
    appropriate brightness range for image display.
        
    Parameters
    ----------
    percentage : float
        Decimal form of percentage above which brightness is retained.
    count : numpy array
        The number of pixels for a given brightness.
    intensity : numpy.ndarray
        The range of brightnesses within the fits image
    Returns
    -------
    vmin : float
        Minimum brightness for jpg display.
    vmax : float
        As above but maximum brightness.
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
    u_img = np.array(img, dtype = np.uint8) #Converting float32 to uint8
    resized_image = cv2.resize(u_img, (round(np.shape(u_img)[1]*h_strch), round(np.shape(u_img)[0]*v_strch))) 
    resized_image = crop(resized_image)

    #This plots a circle for help with stretching (408 and 208 should be replaces with centre)
    #cv2.circle(resized_image,(round(408*h_strch), round(208*v_strch)), 150, (0,255,0), 2)

    return resized_image
        
def arm_drawing(path, save_path, galaxy_name, colour_band, percentage=0.005):
    log_image, vmin, vmax = image_parameters(path, galaxy_name, percentage)
    # Save the FITS display and then grab it immediately after to get a jpeg version
    
    # Displaying initial image
    fig_image = plt.figure(figsize=(10,10))
    ax_image = fig_image.gca()
    ax_image.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
    # ax_image.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
    plt.show() # Currently waits for the rest of the function to run before displaying
    
    while True:
        try:
            arm_count = int(input("How many spiral arms are in the image? "))
            break
        except:
            print("Invalid input, please try again.")
    
    # Drawing
    ix = -1
    iy = -1
    x_list = []
    y_list = []
    global drawing
    drawing = False
      
    def draw(event, x, y, flags, param):
          
        global ix, iy, drawing
          
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix = x
            iy = y            
                  
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.circle(galaxy, (x,y), radius=0, color =(0, 0, 255), thickness =5)
                x_list.append(x)
                y_list.append(y)
          
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
              
    # Loading jpg image for drawing
    galaxy = cv2.imread("Images\\ngc5054bB.jpg")        
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw)
      
    while True:
        cv2.imshow("Image", galaxy)
        # plt.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
          
        if cv2.waitKey(10) == 27:
            break
        
    ymax, xmax, _ = np.shape(galaxy)
    
    fig_points = plt.figure(figsize=(10,10))
    ax_points = fig_points.gca()
    ax_points.plot(x_list, y_list)
    ax_points.set_xlim(0, xmax)
    ax_points.set_ylim(0,  ymax)
    ax_points.set_title("$y$ points versus $x$ points")
    ax_points.set_xlabel("$x$ point")
    ax_points.set_ylabel("$y$ point")
    plt.show()
    
    cv2.destroyAllWindows()
    
    # Make an empty array with number of elements = number of arms
    # Each element is then given a list
    
    return

def image_parameters(path, galaxy_name, percentage):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Calculates the brightness maximum/minimum with which to display the image
    and returns these as well as the image.
    
    Parameters
    ----------
    path : string
        Absolute path where the .fits files are stored. Must not end with \\.
    galaxy_name : string
        The name of the file without the extension, e.g. 'ngc5054b'.
    percentage : float
        Decimal form of percentage above which brightness is retained. Default is 0.5%.

    Returns
    -------
    log_image : numpy array
        2D array containing the brightness information of the image for display
        using plt.imshow
    vmin : float
        Minimum brightness for jpg display.
    vmax : float
        As above but maximum brightness.
    '''
    # Retrieving .fits data and replacing infinities with NaN
    full_image = fits.getdata(str(path)+"\\{}.fits".format(galaxy_name))    
    log_image = np.log10(full_image)
    flattened_log = log_image.flatten()
    flattened_log = np.where(abs(flattened_log) == np.inf, np.nan, flattened_log)
    
    # Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
    # pyplot automatically shows the histogram, which we don't need. Numpy histogram
    # might solve this issue
    fig_hist = plt.figure()
    ax_hist = fig_hist.gca()
    pixel_count, pixel_intensity, _ = plt.hist(flattened_log, bins='auto')
    ax_hist.set_title("Image Histogram")
    plt.close() 
    
    # Giving threshold percentage in decimal form and calculates brightness
    # interval over which to display the image
    vmin, vmax = histogram_limiter(percentage, pixel_count, pixel_intensity)
    
    return log_image, vmin, vmax

def image_display(path, save_path, galaxy_name, colour_band, percentage=0.005):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Plots using plt.imshow from matplotlib and then saves the figure to the
    specified path.
    This function is for when you want to look at the image only, and perform
    no analysis or save it.
    
    Parameters
    ----------
    path : string
        Absolute path where the .fits files are stored. Must not end with \\.
    save_path : string
        Absolute path where to save the jpg images..
    galaxy_name : TYPE
        The name of the file without the extension, e.g. 'ngc5054b'.
    colour_band : float
        Decimal form of percentage above which brightness is retained.
    percentage : float
        Decimal form of percentage above which brightness is retained. Default is 0.5%.

    Returns
    -------
    None.
        
    Example
    -------
         path = "C:\\Users\\Admin\\Documents\\Galaxies"
         save_path = "C:\\Users\\Admin\\Documents\\Galaxy Images"
         galaxy_name = "ngc5054b"
         colour_band = b
         This will grab ngc5054b.fits from the path directory, adjust the
         brightness interval over which to display it according to the 
         brightness histogram, and save a jpg to the save_path directory as
         "ngc5054bB.jpg".
    '''
    '''
    This first name-grabbing section will later need updating to filtering through
    a list of filenames provided to it for each colour band
    ''' 
    # Grabs logarithmic image and minimum and maximum brightness for image display
    log_image, vmin, vmax = image_parameters(path, galaxy_name, percentage)
    
    fig_image = plt.figure(figsize=(10,10))
    ax_image = fig_image.gca()
    
    '''
    TEMPORARY: displaying the log image instead of deprojected image
    '''
    # Replaces log_image with deprojected image and displays it
    depro_image = deprojection(log_image)
    ax_image.imshow(depro_image, cmap='gray', vmin=vmin, vmax=vmax)
    # ax_image.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
    
    # Removing labels for a clean display, then saving the image
    ax_image.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False) 
    ax_image.set_title("{} in {}-Band".format(galaxy_name, colour_band), fontsize=24)
    plt.grid(False)
    # plt.savefig(save_path+"\\{}{}.jpg".format(galaxy_name,colour_band))
    return
