'''
Created on 5. 5. 2017

@author: lada
'''

import numpy as np
from skimage.filter import gabor_kernel #skimage.__version__ if it's lower than 0.11 then use filter instead of filters
from skimage.filter import gabor_filter # gabor in newer versions
from skimage import io
import skimage
import math
import cv2
from scipy import ndimage as ndi

orientations = [0, math.pi/4, math.pi/2, math.pi / 4 * 3]
wavelengths = [0.25, 0.5, 1.0]
sigma = 1

def create_kernels():
    print skimage.__version__
    kernels = []
    
    for theta in orientations:
        #print "Theta: ", theta
        for lambd in wavelengths:
            kernel = gabor_kernel(1.0/lambd, theta=theta, sigma_x=sigma, sigma_y=sigma) # frequency is 1/lambda
            kernels.append(kernel)
           
            #print kernel.shape
            #print kernel
                   
            #io.imshow(np.real(kernel))
            #io.imshow(np.imag(kernel))
            #io.imshow(io.concatenate_images([np.real(kernel), np.imag(kernel)]))      
            #io.show()  
            
            
    return kernels   
    

def show_kernels(kernels, real=True): #if False - show imaginary part
    k_size = kernels[0].shape[0]
    img = np.zeros((k_size * len(wavelengths), k_size * len(orientations)))
       
    #print img.shape
    for i in range(len(kernels)):
        if real:
            k = np.real(kernels[i])
        else:
            k = np.imag(kernels[i])
        n = np.linalg.norm(k) # for normalization
        #print "Norm:", n
        r = i % len(wavelengths)
        c = i / len(wavelengths)
        img[r * k_size : r*k_size + k_size, c*k_size : c*k_size + k_size] = k / n
        
    io.imshow(img)
    io.show()
    
def process_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    responses = []
  
    for theta in orientations:
        for lambd in wavelengths:
            real, imag = gabor_filter(img, 1.0/lambd, theta=theta, sigma_x=sigma, sigma_y=sigma, mode='reflect') # frequency is 1/lambda
            responses.append((real, imag))
            
            #or use ndi.convolve(img, kernel, mode='wrap')
    
    print len(responses)
            
    return responses

    
kernels = create_kernels()

#show_kernels(kernels, real=True)

responses = process_image("img.jpg")
print responses
print len(responses)
print len(responses[0])
io.imshow(responses[11][0])
io.show()
    



    


