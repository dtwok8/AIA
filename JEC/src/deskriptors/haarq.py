import numpy as np
import cv2

img_path = "img.jpg" 
scales = 4

kernel_h = np.array([[1.0, 1.0], [-1.0,-1.0]])
kernel_v = np.array([[-1.0, 1.0], [-1.0,1.0]])
kernel_d = np.array([[1.0, -1.0], [-1.0,1.0]])
kernels = [kernel_h, kernel_v, kernel_d]

def count_haarq(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    size = np.amin(img.shape)
    #print size # prepare 4 scales ->  size * f^3 = 64
    factor = np.power((64.0 / size), 1.0/(scales - 1))
    #print "resize_factor:", factor
        
    vector = np.zeros(scales * len(kernels))
    index = 0
    for scale in range(scales):
        #print "Image shape:", img.shape
        for k in kernels:
            res = cv2.filter2D(img, cv2.CV_16S, k)
            res[res < 0] = -1
            res[res > 0] = 1
            #min = np.amin(res)
            #max = np.amax(res)
            #print min, max, np.average(res)
            vector[index] = np.average(res)
            index += 1
           
        img = cv2.resize(img, (0,0), fx=factor, fy=factor) 
    
    #print vector
    
    return vector