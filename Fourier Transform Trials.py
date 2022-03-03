import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Loads the image and rescales the data using base 10 logarithms
# full_image = fits.getdata("trial_image.fits")
full_image = fits.getdata('trial_image.fits')
log_image = np.log10(full_image)

fig_fourier, ax_fourier = plt.subplots(1,3, figsize=(12,6))
fig_fourier.suptitle("Fourier Transform and Reconstruction of NGC 5054", fontsize=20)
plt.subplots_adjust(wspace=0.3)

# Displaying the unaltered image
ax_fourier[0].imshow(log_image, cmap='gray', vmin=1.5, vmax=2.7)
ax_fourier[0].set_title("Original OSU Image of NGC 5054")

# Fourier transforming the data. Log base 10 is plotted because of the vast
# scale otherwise
image_FFT = np.fft.fftshift(np.fft.fft2(full_image))
filtered_FFT = np.zeros(np.shape(image_FFT))

# Removing some data in Fourier space
FFT_length = np.shape(image_FFT[0])[0]
halfway = int(FFT_length/2)
percentage = 0.1
lower_limit = int(halfway - percentage*FFT_length)
upper_limit = int(halfway + percentage*FFT_length)
filtered_FFT[lower_limit:upper_limit] = image_FFT[lower_limit:upper_limit]
filtered_FFT[:, lower_limit:upper_limit] = image_FFT[:, lower_limit:upper_limit]

ax_fourier[1].imshow(np.log10(abs(filtered_FFT)), cmap='gray')
ax_fourier[1].set_title("2D Fourier Transform of NGC 5054 Image")

# Inverse Fourier transform to reconstruct the original image
image_reconstructed = np.fft.ifft2(filtered_FFT)
ax_fourier[2].imshow(np.log10(abs(image_reconstructed)), cmap='gray', vmin=1.5, vmax=2.7)
ax_fourier[2].set_title("Reconstructed Image of NGC 5054")
plt.tight_layout()
plt.show()