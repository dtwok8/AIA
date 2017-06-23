"""
Vytvari Gabor priznak.

@author: Katerina Kratochvilova
"""

import numpy as np
from skimage.filter import gabor_kernel #skimage.__version__ if it's lower than 0.11 then use filter instead of filters
from skimage.filter import gabor_filter # gabor in newer versions
from skimage import io
import skimage
import math
import cv2
from scipy import ndimage as ndi

#parametry Gabor funkce
orientations = [0, math.pi/4, math.pi/2, math.pi / 4 * 3]
wavelengths = [0.25, 0.5, 1.0]#[4, 4.0 *  math.sqrt(2), 8, 8 *  math.sqrt(2) ]# #[2.0, 2.0 * math.sqrt(2), 4.0] 
sigma = 1

def create_kernels():
    """
        Vytvari kernely (filtry) podle zadanych parametru.
        
        Return: 
            kernels -- vytvorene kernely (filtry).
    """
    #print skimage.__version__
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
    """
        Zobrazi kernely. 
            
        Keyword arguments:
            kernels -- kernely.
            real -- jaka cast se ma zobrazit, pouze realne kernely nabo imaginarni kernely.
    """
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
    
def process_image(img):
    """
        Pouzije filtry na obrazek.
        
        Keyword arguments:
            img -- vstupni obrazek.
        Return:
            responses -- vysledna matice po pouzitych filtrech. 
    """
    responses = []
  
    for theta in orientations:
        for lambd in wavelengths:
            real, imag = gabor_filter(img, 1.0/lambd, theta=theta, sigma_x=sigma, sigma_y=sigma, mode='reflect') # frequency is 1/lambda
            responses.append((real, imag))
            
            #or use ndi.convolve(img, kernel, mode='wrap')
    
    #print len(responses)
            
    return responses


def count_magnitude(filtered_img_real, filtered_img_imag):
    """
        Spocita magnitudu.
        filtered_img_real -- preklopi na osu x, filtered_img_imag preklopi na osu y tim padem mame vektory a spocitame jejich velikost.
        
        Keyword arguments:
            filtered_img_real -- filtrovane obrazky realna cast. 
            filtered_img_imag -- filtrovane obrazky imaginarni cast.
        Return:
            magnitude -- vypoctena magnituda.
    """
    magnitude = []
    
    for i in range(len(filtered_img_real)):
        magnitude.append(cv2.magnitude(filtered_img_real[i], filtered_img_imag[i]))
    
    return magnitude

def count_vector(magnitudes, deep): 
    """
        Nasklada vektory za sebe.
    
        Keyword arguments:
            phase -- faze. 
            deep -- velikost vektrou.
        Return:
            array_histograms_magnitude -- vypocteny vektor.
    """

    array_histograms_magnitude = np.zeros(shape=(deep*len(magnitudes)), dtype=np.int)

    for i in range(len(magnitudes)): 
        for x in range(len(magnitudes[i])):
            for y in range(len(magnitudes[i][x])):
                value = magnitudes[i].item(x,y) 
                index = ((i*deep))+int((value/deep)) # (i*deep) potrebuju se posunout na i-ty filtrovany obrazek
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
    return array_histograms_magnitude

def count_gabor(img):  
    """
        Hlavni metoda pro vypocet gabor.
     
        Keyword arguments:
            img -- vstupni obrazek.
        Return:
            gabor_vector -- vytvoreny priznak.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernels = create_kernels()
    img = img.astype(float)
    #show_kernels(kernels, real=True)

    responses = process_image(img)
    vector_deep = 16
    filtered_img_real = []
    filtered_img_imag = []
    
    for item in responses:
        filtered_img_real.append(item[0])
        filtered_img_imag.append(item[1])
    
    magnitude = count_magnitude(filtered_img_real, filtered_img_imag)
    gabor_vector = count_vector(magnitude, vector_deep)
    return gabor_vector
    #io.imshow(responses[11][0])
    #io.show()
    



    


