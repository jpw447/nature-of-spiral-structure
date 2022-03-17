import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

name = "ic5052b"
band = "B"
computer_path = "C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure"
path = computer_path + "\\OSU\\data\\survey\ByFilter\\{}_band".format(band)

full_image = fits.getdata(str(path)+"\\{}.fits".format(name))    
log_image = np.log10(full_image)

flattened_log = log_image.flatten()
print(np.max(abs(flattened_log)))
# Replace -inf with NaN

# Creates an histogram plot and finds the brightness where most pixels lie (histogram peak)
fig_hist = plt.figure()
ax_hist = fig_hist.gca()
# pixel_count, pixel_intensity, _ = plt.hist(log_image.flatten(), bins='auto')
# ax_hist.set_title("Image Histogram")