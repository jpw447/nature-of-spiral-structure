'''
Base code retrieved from:
https://www.geeksforgeeks.org/drawing-with-mouse-on-images-using-python-opencv/
'''

import cv2
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
  
# img = cv2.imread("gull.jpg")
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

galaxy = cv2.imread("Images\\ngc5054bB.jpg")
ymax, xmax, _ = np.shape(galaxy)
  
# variables
ix = -1
iy = -1
drawing = False
x_list = []
y_list = []
  
def draw_rectangle_with_drag(event, x, y, flags, param):
      
    global ix, iy, drawing, galaxy
      
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

title= "Title of Popup Window"
cv2.namedWindow(winname = title)
cv2.setMouseCallback(title, draw_rectangle_with_drag)
  
while True:
    cv2.imshow("Title of Popup Window", galaxy)
    # plt.imshow(log_image, cmap='gray', vmin=vmin, vmax=vmax)
      
    if cv2.waitKey(10) == 27:
        break

fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.plot(x_list, y_list, 'ro')
ax.set_title("$y$ points versus $x$ points")
ax.set_xlim(0,xmax)
ax.set_ylim(0,ymax)
ax.set_xlabel("$x$ point")
ax.set_ylabel("$y$ point")

cv2.destroyAllWindows()