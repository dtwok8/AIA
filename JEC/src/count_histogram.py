# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np

#moje
import class_pictures
import config



def count_train_histogram():
    """
        Nacte trenovaci seznam obrazku ze souboru. 
        Projde celou trenovaci mnozinu a zavola na vsechny obrazky metody na vypocet histogramu.
        Nasledne ulozi pres metodu do souboru celou strukturu list trenovaci obrazku.
    """
    f = open(config.TRAIN_LIST, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print 'train {}'.format(split_line[0])
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])

        x.rgb = np.array(countRGBHistogram(img), dtype=np.float32)        
        x.lab = np.array(countLABHistogram(img), dtype=np.float32) 
        x.hsv = np.array(countHSVHistogram(img), dtype=np.float32) 
        
        listPictures.append(x)
    f.close()
    
    class_pictures.exportDataToFile(listPictures, config.DATAFILE_TRAIN)


def count_test_histogram():
    """
        Nacte testovaci seznam obrazku ze souboru. 
        Projde celou testovaci mnozinu a zavola na vsechny obrazky metody na vypocet histogramu.
        Nasledne ulozi pres metodu do souboru celou strukturu list testovacich obrazku.
    """
    f = open(config.TEST_LIST, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print 'test {}'.format(split_line[0])
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        x.rgb = np.array(countRGBHistogram(img), dtype=np.float32)        
        x.lab = np.array(countLABHistogram(img), dtype=np.float32) 
        x.hsv = np.array(countHSVHistogram(img), dtype=np.float32) 

        listPictures.append(x)
    
    f.close()
    class_pictures.exportDataToFile(listPictures, config.DATAFILE_TEST)


#def countRGBHistogram(img):
#    array_rgb = np.zeros(shape=(3, 16), dtype=float32)
#    array_pom = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] , dtype=float32)
#
#    print ("------RGB--------")
#    print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))
#
#    for i in (0,1,2):
#        for x in range(len(img)):
#            for y in range(len(img[x])):
#                value = img.item(x,y,i) 
#                index = value/16
#                array_pom[index]=array_pom[index]+1
#        print array_pom
#        array_rgb[i] = array_pom
#        array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#        print "format--------------------------------"
#        print type(array_rgb)
#        print type(array_pom)
#    return array_rgb


def countRGBHistogram(img):
    """
        Spocita rgb na 16 bitovou hloubku pro obrazek poslany v parametru.
        
        Keyword arguments:
            img -- Obrazek pro, ktery se ma histogram vypocitat.
        
        Return:  
            list_rgb -- histogram jako trojrozmerny vektor -list
    """
    list_rgb=[0,0,0]
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#    print ("------RGB--------")
#    print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))

    for i in (0,1,2):
        for x in range(len(img)):
            for y in range(len(img[x])):
                value = img.item(x,y,i) 
                index = value/16
                list[index]=list[index]+1
#        print list
        list_rgb[i] = list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_rgb


def countLABHistogram(img):
    """
        Spocita lab na 16 bitovou hloubku pro obrazek poslany v parametru.
        
        Keyword arguments:
            img -- Obrazek pro, ktery se ma histogram vypocitat.
        
        Return:  
            list_lab -- histogram jako trojrozmerny vektor -list
    """
#    print ("------LAB--------")
    #prevedeni na LAB
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

#    print "shape: "
#    print lab_image.shape
#    print "amin: {}, amax: {}".format(np.amin(lab_image), np.amax(lab_image))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(lab_image[:,:,0]),np.amax(lab_image[:,:,0]),np.amin(lab_image[:,:,1]), np.amax(lab_image[:,:,1]), np.amin(lab_image[:,:,2]), np.amax(lab_image[:,:,1]))
    #l_channel,a_channel,b_channel = cv2.split(lab_image)
    #lab = cv2.split(lab_image)

    list_LAB=[0,0,0]
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in (0,1,2):
        for x in range(len(lab_image)):
            for y in range(len(lab_image[x])):
                value = lab_image.item(x,y,i)
                index = value/16
                list[index]=list[index]+1
        #print list
        list_LAB[i]=list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_LAB

def countHSVHistogram(img):
    """
        Spocita hsv na 16 bitovou hloubku pro obrazek poslany v parametru.
        
        Keyword arguments:
            img -- Obrazek pro, ktery se ma histogram vypocitat.
        
        Return:  
            list_hsv -- histogram jako trojrozmerny vektor -list
    """
#    print ("------HSV--------")
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#    print "amin: {}, amax: {}".format(np.amin(hsv_image), np.amax(hsv_image))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(hsv_image[:,:,0]),np.amax(hsv_image[:,:,0]),np.amin(hsv_image[:,:,1]), np.amax(hsv_image[:,:,1]), np.amin(hsv_image[:,:,2]), np.amax(hsv_image[:,:,1]))
#
#    print hsv_image.shape
#    #hsv = cv2.split(hsv_image)
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    list_hsv=[0,0,0]

    for i in (0,1,2):
        for x in range(len(hsv_image)):
            for y in range(len(hsv_image[x])):
                value = hsv_image.item(x,y,i) 
                index = value/16
                list[index]=list[index]+1
#        print list 
        list_hsv[i]=list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#    print len(hsv_image[0])
#    print len(hsv_image[0][0])
#    print type(hsv_image)
    return list_hsv

#spocita histogramy pro trenovaci mnozinu
#count_train_histogram()
#spocita histogrami pro testovaci mnozinu
count_test_histogram()