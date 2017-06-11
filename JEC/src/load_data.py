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
#import gabor

import deskriptors.poem as poem
import deskriptors.color_poem as color_poem
import deskriptors.haar as haar
import deskriptors.haarq as haarq
import deskriptors.gabor as gabor
import deskriptors.gaborq as gaborq

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
        Zavola prislusne funkce pro spocitani priznaku dle configu.
        
        Keyword arguments:
            picture -- obrazek pro ktery se priznaky pocitaji. 
    """
    img = cv2.imread(picture.name)  
    
    if(config.RGB):
        picture.rgb = count_histogram(img)
        #x.rgb = count_histogram(img) 

    if(config.LAB):
        lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        picture.lab = count_histogram(lab_image)
        #x.lab = count_histogram(lab_image) 
    
    if(config.HSV):
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        picture.hsv = count_histogram(hsv_image)
    
    if(config.GABOR):
        picture.gabor = gabor.count_gabor(img)
    
    if(config.GABORQ):
        picture.gaborq = gaborq.count_gaborq(img)
     
    if(config.POEM):
        picture.poem = poem.count_poem(img)
        
    if(config.COLOR_POEM):
        picture.color_poem = color_poem.count_color_poem(img)
        
    if(config.HAAR):
        picture.haar = haar.count_haar(img)
    
    if(config.HAARQ):
        picture.haarq = haarq.count_haarq(img)

def count_histogram(img, deep = 16):
    """
        Spocita histogram na 16 bitovou hloubku pro obrazek poslany v parametru.
        
        Keyword arguments:
            img -- Obrazek pro, ktery se ma histogram vypocitat.
        
        Return:  
            list_histogram -- histogram jako trojrozmerny vektor -list
    """
   
    histogram_list = [0] * (3*deep)

    for i in (0,1,2):
        for x in range(len(img)):
            for y in range(len(img[x])):
                value = img.item(x,y,i) 
                index = value/deep
                histogram_list[index+(deep*i)]=histogram_list[index+(deep*i)]+1
    histogram = np.asarray(histogram_list, dtype=np.float32)  # kdyz to udelam jako list a pak to prevedu do numpy tak je to o dost rychlejsi           
    return histogram
    
    
load_pictures(config.TRAIN_LIST, config.DATAFILE_TRAIN, "train")
#spocita histogrami pro testovaci mnozin
load_pictures(config.TEST_LIST, config.DATAFILE_TEST, "test")