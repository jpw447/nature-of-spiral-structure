import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def image_display(axis, name, file_name, colour_min=1.7, colour_max=2.7, file_path=''):
    '''
    Loads a FITS file image and rescales it for visualisation using base 10 logarithm.
    Plots using plt.imshow from matplotlib
    '''
    full_image = fits.getdata(file_path+file_name)
    log_image = np.log10(full_image)
    axis.imshow(log_image, cmap='gray', vmin=1.5, vmax=2.7)
    axis.set_title("Original OSU Image of "+name)
    plt.show()
    return full_image

def fourier_transform(image):
    image_FFT = np.fft.fftshift(np.fft.fft2(image))
    return image_FFT
    
def k_space_reduction(axis, name, image_FFT, percentage=0.1):
    '''
    Filters data in Fourier space in the k-direction by twice percentage.
    I.e. 0.1 retains all the data within 20% of maximum kx and maximum ky
    Returns the image Fourier transform as well as plotting the Fourier transform.
    
    Throws an error if above 100% of the image will be transformed - the FT behaves
    strangely in these cases.
    '''
    if percentage > 0.5:
        print("\nInvalid percentage given - must be 0.5 or below.\n")
        return None
    filtered_FFT = np.zeros(np.shape(image_FFT))
    
    FFT_length = np.shape(image[0])[0]
    halfway = int(FFT_length/2)
    lower_limit = int(halfway - percentage*FFT_length)
    upper_limit = int(halfway + percentage*FFT_length)
    filtered_FFT[lower_limit:upper_limit] = image_FFT[lower_limit:upper_limit]
    filtered_FFT[:, lower_limit:upper_limit] = image_FFT[:, lower_limit:upper_limit]
    
    axis.imshow(np.log10(abs(filtered_FFT)), cmap='gray')
    axis.set_title("2D Fourier Transform of "+name+" Image")
    plt.show()
    
    return filtered_FFT

def brightness_reduction(axis, name, image_FFT, threshold):
    '''
    Filters the Fourier transform data to only contain data above a given
    threshold, keeping only the brightest elements
    '''
    absolute_FFT = abs(image_FFT)
    filtered_FFT = np.where(np.log10(absolute_FFT) > threshold*np.max(np.log10(absolute_FFT)), FFT, 0)
    axis.imshow(np.log10(abs(filtered_FFT)), cmap='gray')
    axis.set_title("2D Fourier Transform of "+name+" Image")
    
    return filtered_FFT
    
def image_reconstruction(axis, name, FFT, colour_min=1.7, colour_max=2.7):
    '''
    Uses a given Fourier spectrum to reconstruct an image
    '''
    image_reconstructed = np.fft.ifft2(FFT)
    axis.imshow(np.log10(abs(image_reconstructed)), cmap='gray', vmin=colour_min, vmax=colour_max)
    axis.set_title("Reconstructed Image of "+name)
    plt.show()

# if __name__ == "__main__":
galaxy = "NGC 5054"
fig_fourier, ax_fourier = plt.subplots(1,3, figsize=(12,6))
fig_fourier.suptitle("Fourier Transform and Reconstruction of "+galaxy, fontsize=20)
plt.subplots_adjust(wspace=0.3)

vmin, vmax = 1.7, 2.7   
percentage = 0.1
threshold = 0.7

image = image_display(ax_fourier[0], galaxy, "ngc7412b.fits", vmin, vmax, "OSU\\data\\survey\\ByFilter\\B_band\\")

fig = plt.figure()
hist = plt.hist(image, bins=100)
#%%
'''
Cell containing Fourier transforms of images 
'''
FFT = fourier_transform(image)

# Works fine here, doesn't work within a function and when you call that function

absolute_FFT = abs(FFT)
filtered_FFT = np.where(np.log10(absolute_FFT) > threshold*np.max(np.log10(absolute_FFT)), FFT, 0)

image_reconstructed = np.fft.ifft2(filtered_FFT)
ax_fourier[2].imshow(np.log10(abs(image_reconstructed)), cmap='gray', vmin=1.7, vmax=2.7)
ax_fourier[2].set_title("Reconstructed Image of "+galaxy)

# filtered_FFT = k_space_reduction(ax_fourier[1], galaxy, FFT, percentage)
# filtered_FFT = brightness_reduction(ax_fourier[1], galaxy, FFT, 0.9)

# image_reconstruction(ax_fourier[2], galaxy, filtered_FFT, vmin, vmax)
    
# # Inverse Fourier transform to reconstruct the original image
# image_reconstructed = np.fft.ifft2(filtered_FFT)
# ax_fourier[2].imshow(np.log10(abs(image_reconstructed)), cmap='gray', vmin=1.5, vmax=2.7)
# ax_fourier[2].set_title("Reconstructed Image of NGC 5054")
# plt.tight_layout()
# plt.show()