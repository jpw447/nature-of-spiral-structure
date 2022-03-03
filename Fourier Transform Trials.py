import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Loads the image and rescales the data using base 10 logarithms
# full_image = fits.getdata("trial_image.fits")
full_image = fits.getdata('trial_image.fits')
log_image = np.log10(full_image)

# Displaying the unaltered image
fig_image = plt.figure(figsize=(8,8))
ax_image = fig_image.gca()
ax_image.imshow(log_image, cmap='gray', vmin=1.5, vmax=2.7)
plt.show()

# Fourier transforming the data. Log base 10 is plotted because of the vast
# scale otherwise
image_FFT = np.fft.fftshift(np.fft.fft2(full_image))
fig_FFT = plt.figure(figsize=(8,8))
ax_FFT = fig_FFT.gca()
ax_FFT.imshow(np.log10(abs(image_FFT)), cmap='gray')

# To-do: inverse Fourier transform the FT with some filtering to see what stuff
# corresponds to in the images