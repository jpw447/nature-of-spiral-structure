from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

'''
Following these tutorials:
https://docs.astropy.org/en/stable/io/fits/index.html#f1
https://docs.astropy.org/en/stable/generated/examples/io/plot_fits-image.html#sphx-glr-generated-examples-io-plot-fits-image-py
'''

image = fits.open('frame-u-003918-3-0213.fits')
image.info()
data = image[0].data
print(np.shape(data))

plt.figure()
plt.imshow(data)
plt.colorbar()
plt.show()