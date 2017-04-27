#!/usr/bin/env python
 
import numpy as np
import math
import cv2
 
def build_filters(psi):
    filters = []
    ksize = 7
    sigma = 0.5 
    for theta in (0, math.pi/4, math.pi/2, (3/4)*math.pi):
        for lambdaa in (2, 2*math.sqrt(2), 4): 
            kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambdaa, psi)
            filters.append(kern)

            #kern /= 1.5*kern.sum() #proc? bez toho je jen cerno kdyz mam nasteveny lambdu na 2
    return filters


def use_filters(img, filters):
    filtered_img = []
    
    i=1
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        filtered_img.append(fimg)
        
        cv2.imwrite("gabor_filter_img{}.jpg".format(i), fimg)
        i = i+1
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
    
    return filtered_img
    
    
 
def count_vector(filtered_img, deep = 16): 
    """
    Nasklada vektory za sebe
    """
 
    print len(filtered_img)
    array_histograms_magnitude = np.zeros(shape=(deep*len(filtered_img)), dtype=np.int)

    for i in range(len(filtered_img)): 
        for x in range(len(filtered_img[i])):
            for y in range(len(filtered_img[i][x])):
                value = filtered_img[i].item(x,y) 
                index = ((i*deep))+(value/deep) # (i*deep) potrebuju se posunout na i-ty filtrovany obrazek
                #print index
                #print float_formatter(index)
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
        print array_histograms_magnitude
    return array_histograms_magnitude
    
    
 
img = cv2.imread('P201302280779501.jpg', 0) # 0 Grayscale image 
filters = build_filters(0)

filtered_img = use_filters(img, filters)
count_vector(filtered_img)





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