import numpy as np
import matplotlib.pyplot as plt
from ArmAnalysis import image_display


if __name__ == "__main__":
    fig_image = plt.figure()
    ax_image = fig_image.gca()
    
    galaxy = "NGC 5054"
    vmin = 1
    vmax = 10
    
    path = "C:\\Users\\joepw\\Documents\\Year 3\\Nature of Spiral Structure\\OSU\\data\\survey\\ByFilter\\B_band\\"
    
    image = image_display(ax_image, galaxy, "ngc5054b.fits", vmin, vmax, path)
    
    fig_hist = plt.figure()
    ax_hist = fig_hist.gca()
    histogram = plt.hist(image.flatten())