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
import gabor

import deskriptors.poem as poem
import deskriptors.color_poem as color_poem
import deskriptors.haar as haar
import deskriptors.haarq as haarq

def load_pictures(listImages, outputFile, information):
    """
        Nacte seznam obrazku ze souboru inputFile. 
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
            
        picture = class_pictures.Pictures(split_line[0], split_line[1])
        load_features(picture)
        listPictures.append(picture)
        
    f.close()
    class_pictures.exportDataToFile(listPictures, outputFile)
    
 
def load_features(picture):
    """
        Projde celou mnozinu a zavola na vsechny obrazky metody na vypocet histogramu.
    """
    img = cv2.imread(picture.name)  
    
    if(config.RGB):
        picture.rgb = np.array(count_histogram(img), dtype=np.float32)
        #x.rgb = count_histogram(img) 

    if(config.LAB):
        lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        picture.lab = np.array(count_histogram(lab_image), dtype=np.float32)
        #x.lab = count_histogram(lab_image) 
    
    if(config.HSV):
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        picture.hsv = np.array(count_histogram(hsv_image), dtype=np.float32)
    
    if(config.GABOR):
        picture.gabor = gabor.count_gabor(img)
    
    if(config.GABORQ):
        picture.gabor_q = gabor.count_gabor_q(img)
     
    if(config.POEM):
        picture.poem = poem.count_poem(img)
        
    if(config.COLOR_POEM):
        picture.color_poem = color_poem.count_color_poem(img)
        
    if(config.HAAR):
        picture.haar = haar.count_haar(img)
    
    if(config.HAARQ):
        picture.haarq = haarq.count_haarq(img)

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

    for i in (0,1,2):
        for x in range(len(img)):
            for y in range(len(img[x])):
                value = img.item(x,y,i) 
                index = value/16
                pom_list[index]=pom_list[index]+1
        list_histogram[i] = pom_list
        pom_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_histogram
    
    
#load_pictures(config.TRAIN_LIST, config.DATAFILE_TRAIN, "train")
#spocita histogrami pro testovaci mnozin
load_pictures(config.TEST_LIST, config.DATAFILE_TEST, "test")