# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np


from matplotlib import pyplot as plt
 
 
#moje

img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1210.jpg", 0)


anchor = [ -1, 1 ];
delta = 0;
ddepth = -1;

#kernel = np.ones((5,5),np.float32)/25
#dst = cv2.filter2D(img,ddepth,kernel)
#
#sepFilter2D(source5x5img, dst, deepth, filterX, filterY);

x_kernel = np.array([1.0, 0.0, -1.0]).reshape((1,3))
y_kernel = np.array([1.0, 0.0, -1.0])

gradient =  cv2.sepFilter2D(img, ddepth, x_kernel, y_kernel)
print gradient.shape

gradient = np.zeros((2, img.shape[0], img.shape[1]), dtype = float)
gradient[0,:,:] = cv2.filter2D(img, -1, x_kernel, borderType=cv2.BORDER_REPLICATE) #, dtype = np.float)
gradient[1,:,:] = cv2.filter2D(img, -1, y_kernel, anchor=(-1,0), borderType=cv2.BORDER_REPLICATE) #, dtype = np.float)

#TODO co dela anchor?
print gradient

magnitudy = cv2.magnitude(gradient[0,:,:],gradient[1,:,:])
print magnitudy
print magnitudy.shape

plt.subplot(1,3,1),plt.imshow(gradient[0,:,:],cmap = 'gray')
plt.title('x'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,2),plt.imshow(gradient[1,:,:],cmap = 'gray')
plt.title('y'), plt.xticks([]), plt.yticks([])
plt.subplot(1,3,3),plt.imshow(magnitudy,cmap = 'gray')
plt.title('magnituda'), plt.xticks([]), plt.yticks([]) 

plt.show()
#Compute gradient magnitude at each pixel



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
