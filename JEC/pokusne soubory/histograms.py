# import the necessary packages
import cv2
import numpy as np

#dostanu jen sedou slozku
#gray_img = cv2.imread('P201302280779501.jpg', cv2.IMREAD_GRAYSCALE) 
#cv2.imshow('P201302280779501',gray_img)

#nactu obrazek
img = cv2.imread('../../Data/image_labelling_datasets/iaprtc12/images/00/25.jpg') 


print "calc-hist"
hist = cv2.calcHist([img],[1],None,[256],[0,256])
print hist

#px = img[100,100]
#print px

#blue = img[100,100,0]
#print blue

#print "bincount"
#print np.bincount(img[:,:,0]) #ValueError: object too deep for desired array

print "shape: "
print img.shape
list1=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

print ("------RGB--------")
print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))

for i in (0,1,2):
    for x in range(len(img)):
        for y in range(len(img[x])):
            value = img.item(x,y,i) 
            index = value/16
            list1[index]=list1[index]+1
    print list1 
    list1=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


print ("------LAB--------")
#prevedeni na LAB
lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

print "shape: "
print lab_image.shape
print "amin: {}, amax: {}".format(np.amin(lab_image), np.amax(lab_image))
print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(lab_image[:,:,0]),np.amax(lab_image[:,:,0]),np.amin(lab_image[:,:,1]), np.amax(lab_image[:,:,1]), np.amin(lab_image[:,:,2]), np.amax(lab_image[:,:,1]))
#l_channel,a_channel,b_channel = cv2.split(lab_image)
#lab = cv2.split(lab_image)

list2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in (0,1,2):
    for x in range(len(lab_image)):
        for y in range(len(lab_image[x])):
            value = lab_image.item(x,y,i)
            index = value/16
            list2[index]=list2[index]+1
    print list2 
    list2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#print len(lab_image[0])
#print len(lab_image[0][0])

print ("------HSV--------")
hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

print "amin: {}, amax: {}".format(np.amin(hsv_image), np.amax(hsv_image))
print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(hsv_image[:,:,0]),np.amax(hsv_image[:,:,0]),np.amin(hsv_image[:,:,1]), np.amax(hsv_image[:,:,1]), np.amin(hsv_image[:,:,2]), np.amax(hsv_image[:,:,1]))

print hsv_image.shape
#hsv = cv2.split(hsv_image)
list2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

for i in (0,1,2):
    for x in range(len(hsv_image)):
        for y in range(len(hsv_image[x])):
            value = hsv_image.item(x,y,i) 
            index = value/16
            list2[index]=list2[index]+1
    print list2 
    list2=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
print len(hsv_image[0])
print len(hsv_image[0][0])
print type(hsv_image)

cv2.imshow('P201302280779501',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

