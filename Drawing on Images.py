'''
Base code retrieved from:
https://www.geeksforgeeks.org/drawing-with-mouse-on-images-using-python-opencv/
'''

import cv2
import matplotlib.pyplot as plt
  
img = cv2.imread("gull.jpg")
  
# variables
ix = -1
iy = -1
drawing = False
x_list = []
y_list = []
  
def draw_rectangle_with_drag(event, x, y, flags, param):
      
    global ix, iy, drawing, img
      
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix = x
        iy = y            
              
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x,y), radius=0, color =(0, 0, 255), thickness =5)
            x_list.append(x)
            y_list.append(y)
      
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
          
cv2.namedWindow(winname = "Title of Popup Window")
cv2.setMouseCallback("Title of Popup Window", 
                     draw_rectangle_with_drag)
  
while True:
    cv2.imshow("Title of Popup Window", img)
      
    if cv2.waitKey(10) == 27:
        break
  
plt.plot(x_list, y_list)
plt.title("$y$ points versus $x$ points")
plt.xlabel("$x$ point")
plt.ylabel("$y$ point")

cv2.destroyAllWindows()