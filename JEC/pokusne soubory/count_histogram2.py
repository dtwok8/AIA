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


def load_pictures(listImages, outputFile, information):
    """
        Nacte seznam obrazku ze souboru inputFile. 
        Projde celou mnozinu a zavola na vsechny obrazky metody na vypocet histogramu.
        Nasledne ulozi pres metodu do souboru celou strukturu list testovacich/trenovacich obrazku.
        
        Keyword arguments:
            listImages -- list obrazku 
            outputFile -- nazev souboru do ktereho se maji nactene obrazky ulozit
            information -- debug informace, aby bylo videt co program prave dela
            
    """
    f = open(listImages, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print '{} {}'.format(information, split_line[0])
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        x.rgb = np.array(count_histogram(img), dtype=np.float32)
        #x.rgb = count_histogram(img) 
        
        lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        x.lab = np.array(count_histogram(lab_image), dtype=np.float32)
        #x.lab = count_histogram(lab_image) 

        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        x.hsv = np.array(count_histogram(hsv_image), dtype=np.float32)
        #x.hsv = x.rgb = count_histogram(hsv_image) 

        listPictures.append(x)
    f.close()
    class_pictures.exportDataToFile(listPictures, outputFile)


def count_histogram(img):
    """
        Spocita histogram na 16 bitovou hloubku pro obrazek poslany v parametru.
        
        Keyword arguments:
            img -- Obrazek pro, ktery se ma histogram vypocitat.
        
        Return:  
            list_histogram -- histogram jako trojrozmerny vektor -list
    """
    list_histogram=[0,0,0]
    pom_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#    print ("------RGB--------")
#    print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))

    for i in (0,1,2):
        for x in range(len(img)):
            for y in range(len(img[x])):
                value = img.item(x,y,i) 
                index = value/16
                pom_list[index]=pom_list[index]+1
#        print list
        list_histogram[i] = pom_list
        pom_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_histogram

#def count_histogram(img):
#    array_rgb = np.zeros(shape=(3, 16), dtype=np.float32)
#    array_pom = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] , dtype=np.float32)
#
#    #print ("------RGB--------")
#    #print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
#    #print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))
#
#    print img.shape
#    for i in (0,1,2):
#        print array_pom
#        for x in range(len(img)):  
#            
#            for y in range(len(img[x])):
#                value = img.item(x,y,i)
#                #if(value < 1):
#                    #print i# value/16
#                index = value/16
#                if(i == 1):
#                    index = int(value/16)
#                    #print index
#                    z = z +1
#                    if(z > 13400):
#                        print array_pom
#                        print "z: {} index:{} value: {}".format(z, index, value)
#                        
#                        
#                    if(z > 13500):
#                        exit()
#                    if(z == 13405):
#                        
#                        print array_pom
#                        exit()
#                    
#                array_pom[index]=array_pom[index]+1
#        #print array_pom
#        print array_pom
#        array_rgb[i] = array_pom
#        array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype=np.float32)
#        #print "format--------------------------------"
#        #print type(array_rgb)
#        #print type(array_pom)
#    print "----------- konec metody -----------"
#    return array_rgb

#spocita histogramy pro trenovaci mnozinu
load_pictures(config.TRAIN_LIST, config.DATAFILE_TRAIN, "train")
#spocita histogrami pro testovaci mnozin
load_pictures(config.TEST_LIST, config.DATAFILE_TEST, "test")