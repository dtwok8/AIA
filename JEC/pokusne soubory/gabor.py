#!/usr/bin/env python
 
import numpy as np
import math
import cv2
 
def build_filters(psi):
    filters = []
    ksize = 20
    sigma = 1#0.5 #odchylka gausovky
    gamma = 1 #prostorovy pomer stran (elypsicityda)
    #lambda je vlnova delka
    for theta in (0, math.pi/4, math.pi/2, (3/4)*math.pi): #theta orientace
        #kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, 4, gamma, psi)
        for lambdaa in (2, 2*math.sqrt(2), 4): 
            kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambdaa, gamma, psi)
            #kern /= 1.5*kern.sum() #normovani #proc? bez toho je jen cerno kdyz mam nasteveny lambdu na 2
        filters.append(kern)
    return filters


#def build_filters(psi):
#    filters = []
#    ksize = 7
#    sigma = 0.5 
#    gamma = 1
#    
#    for theta in range(4):
#        theta = theta / 4. * np.pi
#        for sigma in (1, 3):
#
#            for frequency in (0.05, 0.25):
#                kernel = getGaborKernel(frequency, theta=theta, sigma_x=sigma, sigma_y=sigma)
#
#            filters.append(kernel)
#    return filters


def use_filters(img, filters):
    filtered_img = []
    ddepth = -1 #when ddepth=-1, the output image will have the same depth as the source.
    
    i=1
    for kern in filters:
        fimg = cv2.filter2D(img, ddepth, kern)
        filtered_img.append(fimg)
        cv2.imwrite("gabor_filter_img{}.jpg".format(i), fimg)

        i = i+1
    
    return filtered_img
    
    
def count_phase(filtered_img_real, filtered_img_imag):
    phase = []

    for i in range(len(filtered_img_real)):
        cv2.phase(filtered_img_real[i], filtered_img_imag[i], angleInDegrees=False)
        #angleInDegrees - when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    return phase


def count_magnitude(filtered_img_real, filtered_img_imag):
    magnitude = []
    
    for i in range(len(filtered_img_real)):
        magnitude.append(cv2.magnitude(filtered_img_real[i], filtered_img_imag[i]))
    
    return magnitude
    
 
def count_vector(magnitudes, deep): 
    """
    Nasklada vektory za sebe
    """
 
    print len(magnitudes)
    array_histograms_magnitude = np.zeros(shape=(deep*len(magnitudes)), dtype=np.int)

    for i in range(len(magnitudes)): 
        for x in range(len(magnitudes[i])):
            for y in range(len(magnitudes[i][x])):
                value = magnitudes[i].item(x,y) 
                index = ((i*deep))+int((value/deep)) # (i*deep) potrebuju se posunout na i-ty filtrovany obrazek
                print i
                print value
                print index
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
        print array_histograms_magnitude
    return array_histograms_magnitude
    
def show_filters(filters):
    max_value = float('-inf')
    min_value = float('inf')
    
    for filter in filters:
        for i in range(len(filter)):
            for y in range(len(filter[i])):  
                if(filter[i][y] > max_value):
                    max_value = filter[i][y]
                if(filter[i][y] < min_value):
                    min_value = filter[i][y]
    
    n= 0
    for filter in filters:
        for i in range(len(filter)):
            for y in range(len(filter[i])):  
                filter[i][y]=(filter[i][y]-min_value)/(max_value - min_value)*255
        
        cv2.imwrite("gabor_filter{}.jpg".format(n), filter)
        n = n + 1
    
    print max_value
    print min_value
    
 
print "ahoj"
print cv2.magnitude(255, 255)
print math.sqrt(255*255+255*255)

vector_deep = 16
img = cv2.imread('../../Data/iaprtc12/images/03/3117.jpg', 0) # 0 Grayscale image 
img = img.astype(float)

filters_real = build_filters(math.pi/2)
filtered_img = use_filters(img, filters_real)
show_filters(filters_real)
exit()
#count_vector(filtered_img, vector_deep)

filters_imag = build_filters((math.pi/2))

filtered_img_imag = use_filters(img, filters_imag)
filtered_img_real = use_filters(img, filters_real)

magnitudes = count_magnitude(filtered_img_real, filtered_img_imag)
count_vector(magnitudes, vector_deep)

    

phase = count_phase(filtered_img_real, filtered_img_imag)



print filtered_img






# 
#if __name__ == '__main__':
#    import sys
# 
##print __doc__
#try:
#   img_fn = sys.argv[1]
#except:
#   img_fn = 'P201302280779501.jpg'
#
#
#if img is None:
#   print 'Failed to load image file:', img_fn
#   sys.exit(1)




#
#img = cv2.imread('P201302280779501.jpg')
##kern = cv2.getGaborKernel(ksize, sigma, theta (orientation), lambd, gamma[, psi[, ktype]]) 
# 
##fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
#
#    
#fimg = cv2.filter2D(img, -1, kern, borderType=cv2.BORDER_REPLICATE)
#cv2.imshow('result', fimg)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#kern = cv2.getGaborKernel(7, 0.5, math.pi/4, 2, 1) 

#def process(img, filters):
#    accum = np.zeros_like(img) #Return an array of zeros with the same shape and type as a given array.
#    for kern in filters:
#       fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
#       print fimg.shape
#       #spojuje to vsechny filtry dohromady
#       np.maximum(accum, fimg, accum) #Compare two arrays and returns a new array containing the element-wise maxima, prvni dve porovna, tretu accum je pole do kteryho se to vrati
#    return accum
#    #return fimg