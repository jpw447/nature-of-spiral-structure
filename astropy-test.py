from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import numpy as np
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)
'''
Following these tutorials:
https://docs.astropy.org/en/stable/io/fits/index.html#f1
https://docs.astropy.org/en/stable/generated/examples/io/plot_fits-image.html#sphx-glr-generated-examples-io-plot-fits-image-py
https://learn.astropy.org/tutorials/FITS-images.html
'''
# Downloading HorseHead.fits for use
from astropy.utils.data import download_file
image_file = download_file('http://data.astropy.org/tutorials/FITS-images/HorseHead.fits', cache=True )

# Grabs image data and displays it as an image
image_data = fits.getdata(image_file)
plt.figure()
plt.imshow(image_data)
plt.colorbar()

# Histogram plot of the image. Ravel > flatten if you're not using the flattened arraay
# Flatten does this: 
# a = np.array([[1,2], [3,4]])
# a.flatten()
# array([1, 2, 3, 4])
plt.figure()
histogram = plt.hist(image_data.ravel(), bins="auto")
plt.show()

#%%
base_url = 'http://data.astropy.org/tutorials/FITS-images/M13_blue_{0:04d}.fits'

# Imports 5 images and then stores the data for each in a numpy array image_concat
image_list = [download_file(base_url.format(n), cache=True) 
              for n in range(1, 5+1)]
image_concat = [fits.getdata(image) for image in image_list]

# Superposition of the images
final_image = np.sum(image_concat, axis=0)

# Checking the image histogram to decide what limits we should put on the colour scaling
plt.figure()
image_hist = plt.hist(final_image.flatten(), bins='auto')

sketchy_image = plt.figure()
sketchy_image_ax= sketchy_image.gca()
sketchy_image_ax.imshow(final_image, cmap='gray')
sketchy_image_ax.set_title("Image without colour scale limits")

proper_image = plt.figure()
proper_image_ax = proper_image.gca()
proper_image_ax.imshow(final_image, cmap='gray', vmin=2200, vmax=2800)
proper_image_ax.set_title("Image with colour scale limits")