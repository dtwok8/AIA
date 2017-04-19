 
import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/00/51.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2139.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2023.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2157.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/03/3117.jpg")
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2024.jpg")

lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imwrite('img.png', img)

print lab_image.shape
print hsv_image.shape
cv2.imwrite('img0.png', img[:,:,0])
cv2.imwrite('img1.png', img[:,:,1])
cv2.imwrite('img2.png', img[:,:,2])
cv2.imwrite('lab_image.png', lab_image) # ono je klidne mozny ze to umi vykreslovat jen bgr vis

#cv2.imshow("asd", lab_image)

plt.imshow(img)
plt.show()
cv2.waitKey(0)
cv2.imwrite('lab_image0.png', lab_image[:,:,0])
cv2.imwrite('lab_image1.png', lab_image[:,:,1])
cv2.imwrite('lab_imag2.png', lab_image[:,:,2])
cv2.imwrite('hsv_image.png', hsv_image)
cv2.imwrite('hsv_image0.png', hsv_image[:,:,0])
cv2.imwrite('hsv_image1.png', hsv_image[:,:,1])
cv2.imwrite('hsv_image2.png', hsv_image[:,:,2])

exit()

color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()

#img = cv2.imread("P201302280779501.jpg")
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/00/42.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1902.jpg")# papusek
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1516.jpg") #lod
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1515.jpg") #krokodyl
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1579.jpg") #hory
#mg = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/01/1532.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2139.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2023.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2157.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/03/3117.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/27/27000.jpg")
img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/03/3072.jpg")
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2114.jpg")
#img = cv2.imread("../../Data/image_labelling_datasets/iaprtc12/images/02/2054.jpg")
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()


lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()
