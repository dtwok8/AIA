#!/usr/bin/env python
 
import numpy as np
import math
import cv2
 
def build_filters():
#    filters = []
#    ksize = 31
#    for theta in (0, np.pi, np.pi / 16):
#       kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
#       kern /= 1.5*kern.sum()
#       filters.append(kern)
#    return filters

#    filters = []
#    for theta in np.arange(0, np.pi, np.pi / 16):
#        kern = cv2.getGaborKernel((7, 7), 0.5, theta, 2, 1)
#        kern /= 1.5*kern.sum()
#        filters.append(kern)

    filters = []
    ksize = 7
    for theta in (0, math.pi/4, math.pi/2, (3/4)*math.pi):
#       kern = cv2.getGaborKernel((ksize, ksize), 0.5, theta, 2, 0.5)
#       filters.append(kern)
#       kern = cv2.getGaborKernel((ksize, ksize), 0.5, theta, 2*math.sqrt(2), 0.5)
#       filters.append(kern)
       kern = cv2.getGaborKernel((ksize, ksize), 0.5, theta, 4, 0.5)
       print type(kern)

       #kern /= 1.5*kern.sum() #proc? bez toho je jen cerno kdyz mam nasteveny lambdu na 2
       filters.append(kern)
       print len(filters)

    print len(filters)
    return filters
# 
def process(img, filters):
    accum = np.zeros_like(img) #Return an array of zeros with the same shape and type as a given array.
    for kern in filters:
       fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
       print fimg.shape
       #spojuje to vsechny filtry dohromady
       np.maximum(accum, fimg, accum) #Compare two arrays and returns a new array containing the element-wise maxima, prvni dve porovna, tretu accum je pole do kteryho se to vrati
    return accum
    #return fimg

def use_filters(img, filters):
    filtered_img = []
    
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        filtered_img.append(fimg)
        
#        cv2.imshow('filter', fimg)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
    
    return filtered_img
    
    
 
def count_vector(filtered_img, deep = 16): 
    asd = np.array([1, 2, 3])
    print asd
 
    print len(filtered_img)
    array_histograms_magnitude = np.zeros(shape=(deep*len(filtered_img)), dtype=np.int)

    for img in range(len(filtered_img)):
        
        for x in range(len(filtered_img[img])):
            for y in range(len(filtered_img[img][x])):
                value = filtered_img[img].item(x,y) 
                #print value
                #print("{0:.10f}".format(value))
                index = ((img*16))+(value/16)
                #print index
                #print float_formatter(index)
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
        print img
        print array_histograms_magnitude
    print array_histograms_magnitude.shape
    print array_histograms_magnitude
    
    
 
 
 
 
if __name__ == '__main__':
    import sys
 
#print __doc__
try:
   img_fn = sys.argv[1]
except:
   img_fn = 'P201302280779501.jpg'

img = cv2.imread(img_fn, 0) # 0 Grayscale image
if img is None:
   print 'Failed to load image file:', img_fn
   sys.exit(1)

filters = build_filters()

res1 = process(img, filters)
filtered_img = use_filters(img, filters)
count_vector(filtered_img)
cv2.imshow('result', res1)
cv2.waitKey(0)
cv2.destroyAllWindows()

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