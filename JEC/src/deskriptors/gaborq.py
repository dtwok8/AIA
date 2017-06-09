
import numpy as np
from skimage.filter import gabor_kernel #skimage.__version__ if it's lower than 0.11 then use filter instead of filters
from skimage.filter import gabor_filter # gabor in newer versions
from skimage import io
import skimage
import math
import cv2
from scipy import ndimage as ndi

orientations = [0, math.pi/4, math.pi/2, math.pi / 4 * 3]
wavelengths = [2.0, 2.0 * math.sqrt(2), 4.0] #[0.25, 0.5, 1.0]
sigma = 1

def create_kernels():
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
    responses = []
  
    for theta in orientations:
        for lambd in wavelengths:
            real, imag = gabor_filter(img, 1.0/lambd, theta=theta, sigma_x=sigma, sigma_y=sigma, mode='reflect') # frequency is 1/lambda
            responses.append((real, imag))
            
            #or use ndi.convolve(img, kernel, mode='wrap')
    
    #print len(responses)
            
    return responses


def count_magnitude(filtered_img_real, filtered_img_imag):
#    magnitude = []
#    
#    for i in range(len(filtered_img_real)):
#        magnitude.append(cv2.magnitude(filtered_img_real[i], filtered_img_imag[i]))
    magnitude = cv2.magnitude(filtered_img_real, filtered_img_imag)
    return magnitude

def count_vector(phase, deep): 
    """
    Nasklada vektory za sebe
    """

    array_histograms_magnitude = np.zeros(shape=(deep*len(phase)), dtype=np.int)

    #0-360
    #print np.amin(phase)
    #print np.amax(phase)
    #print phase[0].shape
    #print phase[0].shape
    
    for i in range(len(phase)): 
        for x in range(len(phase[i])):
            for y in range(len(phase[i][x])):
                value = (phase[i].item(x,y)-2*math.pi)/(2*math.pi - 0) 
                if(value >= 16): # max by to melo byt 16 rovnych, protoze to je 2pi
                    value = value - 1 #tedy 15
                index = ((i*deep))+int(value) # (i*deep) potrebuju se posunout na i-ty filtrovany obrazek
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
    return array_histograms_magnitude

def count_phase(filtered_img_real, filtered_img_imag):
    #print len(filtered_img_imag)
    #print len(filtered_img_real)
    #print filtered_img_imag[0].shape
    phase = []

    for i in range(len(filtered_img_real)):
        phase.append(cv2.phase(filtered_img_real[i], filtered_img_imag[i], angleInDegrees=False))
        #angleInDegrees - when true, the input angles are measured in degrees, otherwise, they are measured in radians.
        
    return phase

def count_gaborq(img):  
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
    
    phase = count_phase(filtered_img_real, filtered_img_imag)
    gaborq_vector = count_vector(phase, vector_deep)
    return gaborq_vector
    #io.imshow(responses[11][0])
    #io.show()