import numpy as np
import matplotlib.pyplot as plt
import cv2
from astropy.io import fits
import scipy.signal as sc

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
        
def cv2_show_image(title, image):
    '''
    Function used to display images with Open-CV, since this is done repeatedly
    and makes for breaks in the code whilst drawing is conducted. Displays the
    image until the escape key is hit.
    
    Parameters
    ----------
    percentage : string
        Name for the image window.
    count : numpy.ndarray
        The jpg image being displayed.
        
    Returns
    -------
    None.
    
    '''
    while True:
        cv2.imshow(title, image)          
        if cv2.waitKey(10) == 27:
            break
    return

def arm_drawing(path, save_path, file_name, colour_band, percentage=0.005): 
    # Removing band letters from galaxy name for display
    galaxy_name = file_name[:-2]
    
    # Asks the user  to input number of spiral arms, with input control
    while True:
        arm_count = int(input("How many spiral arms are in the image? "))
        if type(arm_count) is not int:
            print("Invalid input, please try again.")
        else:
            break
    # Creating arrays to contain the co-ordinates of each arm
    arms_x = np.empty(shape=(arm_count),dtype=object)
    arms_y = arms_x
    
    # Function define for drawing with the mouse on the image. Has to be defined
    # here or the code doesn't recognise the function.
    # Initialising variables and lists
    ix = -1
    iy = -1
    x_list = []
    y_list = []
    global drawing
    drawing = False
      
    def draw(event, x, y, flags, param):
        # Global variables to grab them from outside function
        global ix, iy, drawing
          
        # When mousebutton is clicked down, draw a circle and save its co-ordinates
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix = x
            iy = y            
            cv2.circle(galaxy, (x,y), radius=0, color =(255, 0, 0), thickness =5)
            x_list.append(x)
            y_list.append(y)
        
        # When mouse is moved, draw a circle and save its co-ordinates
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.circle(galaxy, (x,y), radius=0, color =(255, 0, 0), thickness =5)
                x_list.append(x)
                y_list.append(y)
          
        # When mouse button is lifted up, stop drawing
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
              
    # Loading jpg image for picking out galaxy centre
    print("\n"+path+"\\{}\\{}.jpg".format(galaxy_name, file_name)+"\n")
    galaxy = cv2.imread(path+"\\{}\\{}.jpg".format(galaxy_name, file_name))        
    print("Please pick out the galacitc centre. Only the first pixel will be taken.\nPress escape when you are done.\n")
    window_title = "Galaxy"
    cv2.namedWindow(window_title)
    cv2.setMouseCallback(window_title, draw)
    cv2_show_image(window_title, galaxy)
    
    # Grabbing centre co-ordinates and resetting lists for use
    centre_x, centre_y = x_list[0], y_list[0]
    print("Galactic centre was found at ("+str(centre_x)+","+str(centre_y)+")\n")
    x_list, y_list = [], []
    
    # Aspect ratio 21:9 for figure
    width = 12
    height = width*(9/21)
    
    # Creating figures and axes for plots of each pitch angle
    fig_pa, ax_pa = plt.subplots(1, arm_count, figsize=(width,height))
    # fig_pa.suptitle("{} in {}-band".format(galaxy_name.upper(), colour_band), fontsize=20)
    plt.subplots_adjust(wspace=0.2, top=0.85)
    
    # Drawing and grabbing each spiral arm, depending on how many were specified
    for i in range(0, arm_count):
        print("Draw spiral arm "+str(i+1)+".\n Press escape when you are done.\n")
        cv2_show_image(window_title, galaxy)
        # Converting lists to numpy arrays for calculations
        x_list = np.array(x_list)
        y_list = np.array(y_list)
        # Centering arrays
        x_list -= centre_x
        y_list -= centre_y
        
        # Reflection of y-values
        y_list = -y_list
        
        # Filtering data of noise and picking every 10th point for analysis
        x_list = sc.savgol_filter(x_list, 53, 3)[::10]
        y_list = sc.savgol_filter(y_list, 53, 3)[::10]
        
        # Analysis as in the diary using geometric arguments
        # Mean value between each pair of points
        x_mean = 0.5*(x_list[1:] + x_list[:-1])
        y_mean = 0.5*(y_list[1:] + y_list[:-1])
        
        # Radius
        r_test = np.sqrt(x_mean*x_mean + y_mean*y_mean)
        
        # Triangle sides and pitch angle calculation in degrees
        x_prime = centre_x + (x_list[1:] - x_list[:-1])
        y_prime = centre_y + (y_list[1:] - y_list[:-1])
        r1 = np.sqrt((centre_x - x_prime)**2 + (centre_y - y_prime)**2)
        r2 = np.sqrt((centre_x - x_mean)**2 + (centre_y - y_mean)**2)
        r3 = np.sqrt((x_mean - x_prime)**2 + (y_mean - y_prime)**2)
        
        pitch_angle = 90 - np.arccos((r1**2 + r2**2 - r3**2)/(2*r1*r2)) * 180/np.pi
        
        # print("\n")
        # print(pitch_angle)
        # print("\n")
        
        ax_pa[i].plot(r_test, pitch_angle, 'b')
        ax_pa[i].axis('equal')
        ax_pa[i].set_xlabel("Radius (pixels)", fontsize=15)
        ax_pa[i].set_ylabel("Pitch Angle (°)", fontsize=15)
        ax_pa[i].set_ylim(-90, 90)
        
        with open(save_path+"\\{}\\{}_arm_{}.txt".format(galaxy_name, file_name, i+1), 'w') as text_file:
            for radius, angle in zip(r_test, pitch_angle):
                print("{}\t{}".format(radius, angle), file=text_file)
        
        # Resetting lists for other arms
        x_list, y_list = [], []
    
    # Saving the figures and drawing
    while True:
        save_check = input("Save plots and drawing? Y/N: ").upper()
        
        if save_check == "Y":
            plt.savefig(save_path+"\\{}\\{}_{}-band_plots.eps".format(galaxy_name, file_name, colour_band, colour_band))
            plt.savefig(save_path+"\\{}\\{}_{}-band_plots.png".format(galaxy_name, file_name, colour_band), dpi=300)
            cv2.imwrite(save_path+"\\{}\\{}_{}-band_drawing.png".format(galaxy_name, file_name, colour_band), galaxy)
            break
        
        elif save_check != "N":
            print("Invalid input, please try again.")
            
        else:
            break
        
    # Closing Open-CV windows and Pyplot
    cv2.destroyAllWindows()
    plt.close()
    print("Drawing complete!")
    
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
