import numpy as np
import matplotlib.pyplot as plt
import cv2

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
    
if __name__ == "__main__": 
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
          
        global ix, iy, drawing
          
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix = x
            iy = y            
            cv2.circle(galaxy, (x,y), radius=0, color =(0, 0, 255), thickness =5)
            x_list.append(x)
            y_list.append(y)
                  
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.circle(galaxy, (x,y), radius=0, color =(0, 0, 255), thickness =5)
                x_list.append(x)
                y_list.append(y)
          
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
              
    # Loading jpg image for picking out galaxy centre
    galaxy = cv2.imread("Images\\Pure Logarithmic Spiral.jpg")        
    print("Please pick out the galacitc centre. Only the first pixel will be taken.\nPress escape when you are done.\n")
    window_title = "Galaxy"
    cv2.namedWindow(window_title)
    cv2.setMouseCallback(window_title, draw)
    
    cv2_show_image(window_title, galaxy)
    
    # Grabbing centre co-ordinates and resetting lists for use
    centre_x_test, centre_y_test = x_list[0], y_list[0]
    print("Galactic centre was found at ("+str(centre_x_test)+","+str(centre_y_test)+")\n")
    x_list, y_list = [], []
        
    ###### Pure Spiral Test only section ######
    fig_checker = plt.figure()
    ax_checker = fig_checker.gca()
    #####################
    
    # Drawing and grabbing each spiral arm, depending on how many were specified
    for i in range(0, arm_count):
        print("Draw spiral arm "+str(i+1)+".\n Press escape when you are done.\n")
        cv2_show_image(window_title, galaxy)
        # Converting lists to numpy arrays for calculations
        x_list = np.array(x_list)
        y_list = np.array(y_list)
        # Centering arrays
        x_list -= centre_x_test
        y_list -= centre_y_test
        
        # Reflection of y-values
        y_list = -y_list
        
        r_test = np.sqrt(x_list*x_list + y_list*y_list)
        
        ###### Pure Spiral Test only section ######
        ax_checker.plot(r_test)
        ax_checker.axis('equal')
        ax_checker.set_xlabel("Index")
        ax_checker.set_ylabel("$r$")
        ax_checker.set_title("Radius $r$ as a function of array index")
        #####################
        
        x_list, y_list = [], []
        
    # Closing Open-CV windows and proceeding to analysis
    # cv2.destroyAllWindows()
    print("Drawing complete!")
