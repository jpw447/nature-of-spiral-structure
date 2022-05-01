import cv2
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
  
'''
This code was used to develop the digital image tracing, and not for
pitch angle calculation development. 

The file can be run as long as the pathway and a valid image is provided
(lines 20-23).

This file is considered redundant and is kept only for a historical record.

Base code retrieved from:
https://www.geeksforgeeks.org/drawing-with-mouse-on-images-using-python-opencv/
'''

if __name__ == "__main__":
    # img = cv2.imread("gull.jpg")
    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    galaxy_name = "NGC 5054 CV2.jpg"
    galaxy = cv2.imread("Images\\ngc5054bB.jpg")
    ymax, xmax, _ = np.shape(galaxy)
      
    # variables
    ix = -1
    iy = -1
    drawing = False
    x_list = []
    y_list = []
      
    def draw_rectangle_with_drag(event, x, y, flags, param):  
        '''
        This function  allows OpenCV to draw on the image when the mouse button is
        clicked and moves. The mouse has to be clicked and dragged to produce
        spots.
        '''
        global ix, iy, drawing, galaxy
          
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix = x
            iy = y            
                  
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                cv2.circle(galaxy, (x,y), radius=0, color =(255, 0, 0), thickness =5)
                x_list.append(x)
                y_list.append(y)
          
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
    
    # Creating OpenCV window for image
    title= "Title of Popup Window"
    cv2.namedWindow(winname = title)
    cv2.setMouseCallback(title, draw_rectangle_with_drag)
      
    # Displaying the image until the user hits "escape" on their keyboard
    while True:
        cv2.imshow("Title of Popup Window", galaxy)
          
        if cv2.waitKey(10) == 27:
            break
        
    # Saves the image with the drawing on it
    cv2.imwrite(galaxy_name, galaxy)
    
    # Plot to reproduce the drawn points
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca()
    ax.plot(x_list, y_list, 'ro')
    ax.set_title("$y$ points versus $x$ points")
    ax.set_xlim(0,xmax)
    ax.set_ylim(0,ymax)
    ax.set_xlabel("$x$ point")
    ax.set_ylabel("$y$ point")
    
    # Closes all OpenCV windows (i.e. the image)
    cv2.destroyAllWindows()