 
import numpy as np
import math
import cv2
 
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg", 0)

def count_gradient(img):
    anchor = [ -1, 1 ];
    delta = 0;
    ddepth = -1;

    x_kernel = np.array([1.0, 0.0, -1.0]).reshape((1,3))
    y_kernel = np.array([1.0, 0.0, -1.0])

    gradient =  cv2.sepFilter2D(img, ddepth, x_kernel, y_kernel)
    print gradient.shape

    gradient = np.zeros((3, img.shape[0], img.shape[1]), dtype = float)
    gradient[0,:,:] = cv2.filter2D(img, -1, x_kernel, borderType=cv2.BORDER_REPLICATE) #, dtype = np.float)
    gradient[1,:,:] = cv2.filter2D(img, -1, y_kernel, anchor=(-1,0), borderType=cv2.BORDER_REPLICATE) #, dtype = np.float)
    return gradient


def count_magnitude1(gradient):
    magnitude = cv2.magnitude(gradient[0],gradient[1])
    return magnitude

def count_magnitude2(gradient): 
    magnitude=np.sqrt(gradient[0,:,:]*gradient[0,:,:]+gradient[1,:,:]*gradient[1,:,:])
    return magnitude

def count_magnitude3(gradient):
    magnitude = np.zeros((gradient[0].shape), dtype = float)
    
    for x in range(len(gradient[0])):
        for y in range(len(gradient[0][x])):
            magnitude[x][y] = math.sqrt(gradient.item(0, x, y) * gradient.item(0, x, y) + gradient.item(1, x, y) * gradient.item(1, x, y))
    
    return magnitude
    
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/00/51.jpg", 0) # 0 nacitame cernobili obrazek
gradient = count_gradient(img)
magnitude1 = count_magnitude1(gradient) 
magnitude2 = count_magnitude2(gradient)
magnitude3 = count_magnitude3(gradient)

for i in range(len(magnitude1)):
    for y in range(len(magnitude1[0])):
        if(magnitude1[i][y] != magnitude2[i][y]):
            print "NESHODUJE SE"
            exit()
    
cv2.imwrite('magnitude3.png', magnitude3)
cv2.imwrite('magnitude1.png', magnitude1)
cv2.imwrite('magnitude2.png', magnitude2)
cv2.imwrite('gradientX.png', gradient[0,:,:])
cv2.imwrite('gradientY.png', gradient[1,:,:])