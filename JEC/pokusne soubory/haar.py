import numpy as np
import cv2

img_path = "img.jpg" 
scales = 4

kernel_h = np.array([[1.0, 1.0], [-1.0,-1.0]])
kernel_v = np.array([[-1.0, 1.0], [-1.0,1.0]])
kernel_d = np.array([[1.0, -1.0], [-1.0,1.0]])
kernels = [kernel_h, kernel_v, kernel_d]

def haar_1(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    size = np.amin(img.shape)
    print size # prepare 4 scales ->  size * f^3 = 64
    factor = np.power((64.0 / size), 1.0/(scales - 1))
    print "resize_factor:", factor
       
    vector = np.zeros(scales * len(kernels))
    index = 0
    for scale in range(scales):
        #print "Image shape:", img.shape
        for k in kernels:
            res = cv2.filter2D(img, cv2.CV_16S, k)
            #min = np.amin(res)
            #max = np.amax(res)
            #print min, max, np.average(res)
            vector[index] = np.average(res)
            index += 1
            cv2.imwrite('haar.jpg', res)
           
        img = cv2.resize(img, (0,0), fx=factor, fy=factor) 
    
    print vector
    
    cv2.imwrite('haar.jpg', res)
#    io.imshow(res)
#    io.show()
    
    
    #print res
    
    return vector

haar_1(img_path)