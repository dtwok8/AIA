import numpy as np
import cv2

img_path = "img.jpg" 
scales = 4

kernel_h = np.array([[1.0, 1.0], [-1.0,-1.0]])
kernel_v = np.array([[-1.0, 1.0], [-1.0,1.0]])
kernel_d = np.array([[1.0, -1.0], [-1.0,1.0]])
kernels = [kernel_h, kernel_v, kernel_d]

def count_histogram(index, histogram, array, deep=16):
    #histogram = np.zeros((deep,), dtype=np.int)
    
    max = np.amax(array)
    min = np.amin(array)
    
    for row in array:
        for item in row:
            #print item
            #print item, min, max
            i = (((item-min)/(max-min))*16)-1
            histogram[deep*index+i] = histogram[deep*index+i] + 1

    return histogram
    

def count_haar(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    size = np.amin(img.shape)
    #print size # prepare 4 scales ->  size * f^3 = 64
    factor = np.power((64.0 / size), 1.0/(scales - 1))
    #print "resize_factor:", factor
       
    vector = np.zeros(scales * len(kernels))

    histogram = np.zeros((scales*len(kernels)*16), dtype=np.int)
    
    index = 0
    for scale in range(scales):
        #print "Image shape:", img.shape
        for k in kernels:
            res = cv2.filter2D(img, cv2.CV_16S, k)
            #vector[index] = np.average(res)
            count_histogram(index,histogram,res)
            index += 1
            #cv2.imwrite('haar.jpg', res)
            
            
        img = cv2.resize(img, (0,0), fx=factor, fy=factor) 
    
    #print histogram
    #print vector
    
    #cv2.imwrite('haar.jpg', res)
#    io.imshow(res)
#    io.show()
    
    
    #print res
    return histogram
    #return vector

#img = cv2.imread("img.jpg") 
#count_haar(img)