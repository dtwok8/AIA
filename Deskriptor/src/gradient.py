# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np


from matplotlib import pyplot as plt
 
 
def count_gradient(img):
#    anchor = [ -1, 1 ];
#    delta = 0;
#    ddepth = -1;

#    x_kernel = np.array([1.0, 0.0, -1.0]).reshape((1,3))
#    y_kernel = np.array([1.0, 0.0, -1.0])
    x_kernel = np.array([-1.0, 1.0]).reshape((1,2))
    y_kernel = np.array([-1.0, 1.0])
    img = img.astype(float)
    gradient = np.zeros((2, img.shape[0], img.shape[1]), dtype = float)
    gradient[0,:,:] = cv2.filter2D(img, -1, x_kernel, borderType=cv2.BORDER_REPLICATE)
    gradient[1,:,:] = cv2.filter2D(img, -1, y_kernel, borderType=cv2.BORDER_REPLICATE)
    print gradient[0,:,:]
    #exit()
    return gradient
    
def count_magnitude(gradient):
    magnitude = cv2.magnitude(gradient[0,:,:],gradient[1,:,:])
    print magnitude
    return magnitude



def smer(img, gradient):
    #Compute gradient magnitude at each pixel
    directions = 3
    bin_size = 2 * np.pi / directions
    directional = np.zeros((directions, img.shape[0], img.shape[1]), dtype=float)

    dirs = np.arctan2(gradient[0,:,:], gradient[1,:,:]) + np.pi - np.pi / 1000000


    dirs[dirs < 0] = 0
    mags = np.sqrt(gradient[0,:,:]**2 + gradient[1,:,:]**2) #znova pocitam magnitudu ?

    for d in range(directions):
          lower = d * bin_size
          upper = (d + 1) * bin_size
          directional[d] = dirs
          directional[d][directional[d] < lower] = 0
          directional[d][directional[d] > upper] = 0
          directional[d][directional[d] > 0] = 1 
          directional[d] *= mags

    print directional


def compute_direction(directions, gradient, magnitude):
    dirs = np.arctan2(gradient[0,:,:], gradient[1,:,:]) * 180 / np.pi # vypocte to úhel
    
    soubor = open("uhly.txt", 'w')  
    for row in dirs:
        for item in row:
            soubor.write(" {} ".format(item))
        soubor.write("\n")
    soubor.close()
    directional = np.zeros((directions, gradient[0].shape[0], gradient[0].shape[1]), dtype=float)
    
    for i in range(len(dirs)):
        for y in range(len(dirs[i])):
            if(dirs[i][y] < 0):
                dirs[i][y] = 360 - dirs[i][y]
                print "prevadime"
            if(dirs[i][y] >= 0 and dirs[i][y] < 120):
                directional[0][i][y] = magnitude[i][y]
            if(dirs[i][y] >= 120 and dirs[i][y] < 270):
                directional[1][i][y] = magnitude[i][y]
            if(dirs[i][y] >= 270 and dirs[i][y] < 360):
                directional[2][i][y] = magnitude[i][y]    

    return directional

def compute_aems(directional, img):
    cell_size = 7
    directions = 3
    # use either convolution or integral image
    kernel = np.ones((cell_size, cell_size))
    aems = np.zeros((directions, img.shape[0], img.shape[1]), dtype=float)
    for d in range(directions):
        aems[d, :, :] = cv2.filter2D(directional[d, :, :], -1, kernel, borderType=cv2.BORDER_REPLICATE)
    
    return aems
    
        
def compute_lbp(directions, aems):
    block_size = 10
    bordersize = block_size / 2 + 1
    
    lbp = np.zeros(aems.shape, dtype=np.uint8)
    for d in range(directions):
        border_img = cv2.copyMakeBorder(aems[d, :, :], top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_REPLICATE)

        for r in range(bordersize, border_img.shape[0] - bordersize):
            #print r
            for c in range(bordersize, border_img.shape[1] - bordersize):
                #print r, c
                lbp[d, r - bordersize, c - bordersize] = compute_lbp_value(r, c, border_img)
                #break
            #break
        #break
    return lbp


def compute_lbp_value(r, c, border_img):
    block_size = 10
    radius = float(block_size) / 2
    tau = 4
    #print "diameter:", r
    val = 0
    center = border_img[r, c]
    #print "Computing lbp val for", repr(r), repr(c), "center val:", center
    for i in range(8):
        x = np.cos(i * 2 * np.pi / 8) * radius
        y = np.sin(i * 2 * np.pi / 8) * radius
        #print x, y
        if False: # self.interpolation:      
            v = 0#interpolate(c + x, r - y, border_img)
        else:
            v = border_img[int(y), int(x)]
            #print "value", v
        #if (v - center) >= self.tau:
        #  val += 1
        #val = val << 1;   
        if (v - center) >= tau:       
            val += np.power(2, i)
        #print "akt lbp val:", val
    return val


img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg", 0)
img = np.float32(img) / 255.0
img = np.array([[8, 7, 5, 5], [8, 7, 5, 5],[1,2,4, 4],[3, 5, 7, 7], [3, 5, 7, 5]], dtype= np.uint8)
gradient = count_gradient(img)
magnitude = count_magnitude(gradient) 
cv2.imwrite('gradientX.png', gradient[0,:,:])
cv2.imwrite('gradientY.png', gradient[1,:,:])
cv2.imwrite('magnitude.png', magnitude)

directions = 3
directional = compute_direction(directions, gradient, magnitude)
cv2.imwrite('directional1.png', directional[0,:,:])
cv2.imwrite('directional2.png', directional[1,:,:])
cv2.imwrite('directional3.png', directional[2,:,:])

phase = cv2.phase(gradient[0,:,:], gradient[1,:,:])
print phase

exit()
aems = compute_aems(directional, img)
lbp = compute_lbp(directions, aems)

print lbp.shape
print lbp

cv2.imwrite('lbp.png', lbp[0,:,:])

soubor = open("gradient0.txt", 'w')

for row in gradient[0]:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()

soubor = open("gradient1.txt", 'w')  
for row in gradient[1]:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()
        
soubor.close()

soubor = open("img.txt", 'w')  
for row in img:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()



# Python gradient calculation 
print "---------------------------------" 
# Read image
img = cv2.imread('../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg', 0)
img = np.float32(img) / 255.0
 
# Calculate gradient 
gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)

# Python Calculate gradient magnitude and direction ( in degrees ) 
mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

print angle.shape
print mag.shape

soubor = open("angle.txt", 'w')  
for row in angle:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()

soubor = open("mag.txt", 'w')  
for row in mag:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()
exit()
#smery = compute_direction(directions, gradient, mag)
#print smery.shape

directional = np.zeros((3, 360, 480), dtype=float)
print angle.shape
print directional.shape
for i in range(len(angle)):
    for y in range(len(angle[i])):
        if(angle[i][y] >= 0 and angle[i][y] < 120):
            directional[0][i][y] = magnitude[i][y]
        if(angle[i][y] >= 120 and angle[i][y] < 270):
            directional[1][i][y] = magnitude[i][y]
        if(angle[i][y] >= 270 and angle[i][y] < 360):
            directional[2][i][y] = magnitude[i][y] 
                
cv2.imwrite('directional1.png', directional[0,:,:])
cv2.imwrite('directional2.png', directional[1,:,:])
cv2.imwrite('directional3.png', directional[2,:,:])
                
exit()

#Compute gradient magnitude at each pixel

bin_size = 2 * np.pi / directions
directional = np.zeros((directions, img.shape[0], img.shape[1]), dtype=float)

x = np.array([-1, +1, +1, -1])
y = np.array([-1, -1, +1, +1])
asd = np.arctan2(y, x) * 180 / np.pi
print asd


print dirs

# do jakeho kvadrantu to patri bezva porad mi vychazi jen ten prvni
print dirs.shape
#print "{} {} {}".format(gradient[0,350,479], gradient[1,350,479], dirs[350,479])

 




exit()
dirs[dirs < 0] = 0
mags = np.sqrt(gradient[0,:,:]**2 + gradient[1,:,:]**2) #znova pocitam magnitudu ?

for d in range(directions):
      lower = d * bin_size
      upper = (d + 1) * bin_size
      directional[d] = dirs
      directional[d][directional[d] < lower] = 0
      directional[d][directional[d] > upper] = 0
      directional[d][directional[d] > 0] = 1 
      directional[d] *= mags

print directional

    
    
cv2.imwrite('directional1.png', directional[0,:,:])
cv2.imwrite('directional2.png', directional[1,:,:])
cv2.imwrite('directional3.png', directional[2,:,:])

#cv2.sepFilter2D(src, ddepth, kernelX, kernelY)
#print kernel
#print cv2.sepFilter2D(img, ddepth, [1, -1], [[1], [-1]])


#print cv2.magnitude(x[:,:,0],y[:,:,1]) 
 
 
 
 
# 
# 
# 
# 
# 
#img = cv2.imread('../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg',0)
#
#laplacian = cv2.Laplacian(img,cv2.CV_64F)
#sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
#sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
#
#print laplacian.shape
#
#plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
#plt.title('Original'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
#plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
#plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
#plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
#plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
#
#plt.show()
#
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg", 0)
#    
#  # Output dtype = cv2.CV_8U
#sobelx8u = cv2.Sobel(img,cv2.CV_8U,1,0,ksize=5)
#
## Output dtype = cv2.CV_64F. Then take its absolute and convert to cv2.CV_8U
#sobelx64f = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
#abs_sobel64f = np.absolute(sobelx64f)
#sobel_8u = np.uint8(abs_sobel64f)
#
#
##MAGNITUDA
##print cv2.magnitude()
#
#plt.subplot(1,3,1),plt.imshow(img,cmap = 'gray')
#plt.title('Original'), plt.xticks([]), plt.yticks([])
#plt.subplot(1,3,2),plt.imshow(sobelx8u,cmap = 'gray')
#plt.title('Sobel CV_8U'), plt.xticks([]), plt.yticks([])
#plt.subplot(1,3,3),plt.imshow(sobel_8u,cmap = 'gray')
#plt.title('Sobel abs(CV_64F)'), plt.xticks([]), plt.yticks([]) 
#plt.show()
#
#img = cv2.imread('../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg',0)
#f = np.fft.fft2(img)
#fshift = np.fft.fftshift(f)
#magnitude_spectrum = 20*np.log(np.abs(fshift))
#
#plt.subplot(121),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
#plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()
#
#
#
#img = cv2.imread('../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg',0)
#
#img_float32 = np.float32(img)
#
#dft = cv2.dft(img_float32, flags = cv2.DFT_COMPLEX_OUTPUT)
#dft_shift = np.fft.fftshift(dft)
#
#magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
#
#plt.subplot(121),plt.imshow(img, cmap = 'gray')
#plt.title('Input Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
#plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
#plt.show()  
#
#
#
