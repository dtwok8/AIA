# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi testovacima histogramama a testovacima histograma. Naskaluje vysledky na 0-1. Slozi dohromady jednotlive vysledky (JEC)
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np
import math

from operator import attrgetter #sorter

#moje
import class_pictures
import class_neighbor
import config
import label_transfer


def count_distance(train_data, test_image):
    print test_image.name
    print test_image.keywords
    #potrebujeme zjistit rozdahy kvuli skalovatelnosti, sice je to neprehledne ale usetrime si dalsi tri cykly
    rgb_min=float("inf")
    rgb_max=float("-inf")
    lab_min=float("inf")
    lab_max=float("-inf")
    hsv_min=float("inf")
    hsv_max=float("-inf")
    gabor_min = float("inf")
    gabor_max = float("-inf")
    gaborq_min = float("inf")
    gaborq_max = float("-inf")
    poem_min = float("inf")
    poem_max = float("-inf")
    color_poem_min = float("inf")
    color_poem_max = float("-inf")
    haar_min = float("inf")
    haar_max = float("-inf")
    haarq_min = float("inf")
    haarq_max = float("-inf")
    #print ( rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)
    #print ( rgb_max , rgb_min, lab_max > 3333.72839, lab_min, hsv_max, hsv_min)
    #test_image.neighbors  = []
    pom_nei = []   
    #spocitame vzdalenosti mezi testovacim obrazkem a tranovaci mnozinou
    #zaroven spocitame minmum a maximum pro dany testovaci obrazek
    for picture in train_data:
        pom_neighbor = class_neighbor.Neighbor(picture)
        
        if(config.RGB):    
            pom_neighbor.rgb_distance = cv2.norm(picture.rgb, test_image.rgb, config.RGB_DISTANCE)
            if(pom_neighbor.rgb_distance < rgb_min):
                rgb_min = pom_neighbor.rgb_distance
            if(pom_neighbor.rgb_distance > rgb_max):
                rgb_max = pom_neighbor.rgb_distance
        
        if(config.LAB):
            pom_neighbor.lab_distance  = cv2.compareHist(picture.lab, test_image.lab, cv2.HISTCMP_KL_DIV) #kl(picture.lab, test_image.lab)#            
            if(pom_neighbor.lab_distance < lab_min):
                lab_min = pom_neighbor.lab_distance
            if(pom_neighbor.lab_distance > lab_max):
                lab_max = pom_neighbor.lab_distance        
        
        if(config.HSV):
            pom_neighbor.hsv_distance = cv2.norm(picture.hsv, test_image.hsv, config.RGB_DISTANCE)
            if(pom_neighbor.hsv_distance < hsv_min):
                hsv_min = pom_neighbor.hsv_distance
            if(pom_neighbor.hsv_distance > hsv_max):
                hsv_max = pom_neighbor.hsv_distance
        
        if(config.GABOR):
            pom_neighbor.gabor_distance = cv2.norm(picture.gabor, test_image.gabor, cv2.NORM_L1)
            if(pom_neighbor.gabor_distance < gabor_min):
                gabor_min = pom_neighbor.gabor_distance
            if(pom_neighbor.gabor_distance > gabor_max):
                gabor_max = pom_neighbor.gabor_distance 
                
        if(config.GABORQ):
            if(picture.gaborq.shape != test_image.gaborq.shape):
                print "divny"
                continue
            
            print picture.gaborq.shape, test_image.gaborq.shape
            print picture.name
            pom_neighbor.gaborq_distance = cv2.norm(picture.gaborq, test_image.gaborq, cv2.NORM_L1)
            
            if(pom_neighbor.gaborq_distance < gaborq_min):
                gaborq_min = pom_neighbor.gaborq_distance
            if(pom_neighbor.gaborq_distance > gaborq_max):
                gaborq_max = pom_neighbor.gaborq_distance 
                
        if(config.POEM):            
            #pom_neighbor.poem_distance = cv2.norm(picture.poem, test_image.poem, cv2.NORM_L1)
            pom_neighbor.poem_distance = cv2.compareHist(picture.poem.astype(np.float32), test_image.poem.astype(np.float32), cv2.HISTCMP_INTERSECT)
            #pom_neighbor.poem_distance = cv2.compareHist(np.zeros(16, dtype=np.float32), np.zeros(16, dtype=np.float32), cv2.HISTCMP_KL_DIV)
            if(pom_neighbor.poem_distance < poem_min):
                poem_min = pom_neighbor.poem_distance
            if(pom_neighbor.poem_distance > poem_max):
                poem_max = pom_neighbor.poem_distance 
        
        if(config.COLOR_POEM):
            pom_neighbor.color_poem_distance = cv2.norm(picture.color_poem, test_image.color_poem, cv2.NORM_L1)
            if(pom_neighbor.color_poem_distance < color_poem_min):
                color_poem_min = pom_neighbor.color_poem_distance
            if(pom_neighbor.color_poem_distance > color_poem_max):
                color_poem_max = pom_neighbor.color_poem_distance     
        
        if(config.HAAR):
            pom_neighbor.haar_distance = cv2.norm(picture.haar, test_image.haar, cv2.NORM_L1)
            if(pom_neighbor.haar_distance < haar_min):
                haar_min = pom_neighbor.haar_distance
            if(pom_neighbor.haar_distance > haar_max):
                haar_max = pom_neighbor.haar_distance 

        if(config.HAARQ):
            pom_neighbor.haarq_distance = cv2.norm(picture.haarq, test_image.haarq, cv2.NORM_L1)
            if(pom_neighbor.haarq_distance < haarq_min):
                haarq_min = pom_neighbor.haarq_distance
            if(pom_neighbor.haarq_distance > haarq_max):
                haarq_max = pom_neighbor.haarq_distance 
                
        pom_nei.append(pom_neighbor) #pridani souseda

    count_jec(pom_nei,test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min, gabor_max, gabor_min, gaborq_max, gaborq_min,poem_max, poem_min, color_poem_max, color_poem_min, haar_max, haar_min, haarq_max, haarq_min) 
    
    keywords_prepare_sort=[]
    for neighbor in pom_nei:
        keywords_prepare_sort.append([neighbor, neighbor.jec]) 

    keywords_prepare_sort = sorted(keywords_prepare_sort, key=getKey, reverse=False)

    item.nereast_neighbors = keywords_prepare_sort[0:config.COUNT_NEIGHBORS]

def count_n():
    n = 0
    if(config.RGB):
        n = n +1
        
    if(config.LAB):
        n = n + 1
        
    if(config.HSV):
        n = n + 1
        
    if(config.GABOR):
        n = n + 1
        
    if(config.GABORQ):
        n = n + 1
    
    if(config.POEM):
        n = n + 1
    
    if(config.COLOR_POEM):
        n = n + 1
    
    if(config.HAAR):
        n = n + 1
    
    if(config.HAARQ):
        n = n + 1
        
    return n

#spocita JEC pro tri parametry rgb, hsv, lab, ty to musíš naškálovat od 0 o 1 takže asi ten jec můžeš počítat stejně až budeš mít všechny ty výsledky
def count_jec(pom_nei, test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min, gabor_max, gabor_min, gaborq_max, gaborq_min, poem_max, poem_min, color_poem_max, color_poem_min, haar_max, haar_min, haarq_max, haarq_min):
    #print ( rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)
    n = count_n()

    for neighbor in pom_nei:
        sum_distance = 0
        #naskalovani na 0 - 1
        if(config.RGB == True):
            neighbor.rgb_distance_scale = (neighbor.rgb_distance-rgb_min)/((rgb_max - rgb_min))
            sum_distance = sum_distance + neighbor.rgb_distance_scale

        if(config.LAB == True):
            neighbor.lab_distance_scale = (neighbor.lab_distance-lab_min)/((lab_max - lab_min)) 
            sum_distance = sum_distance + neighbor.lab_distance_scale

        if(config.HSV == True):
            neighbor.hsv_distance_scale = (neighbor.hsv_distance-hsv_min)/((hsv_max - hsv_min))
            sum_distance = sum_distance + neighbor.hsv_distance_scale
            
        if(config.GABOR):
            neighbor.gabor_distance_scale = (neighbor.gabor_distance - gabor_min)/(gabor_max - gabor_min)
            sum_distance = sum_distance + neighbor.gabor_distance_scale
        
        if(config.GABORQ):
            neighbor.gaborq_distance_scale = (neighbor.gaborq_distance - gaborq_min)/(gaborq_max - gaborq_min)
            sum_distance = sum_distance + neighbor.gaborq_distance_scale
        
        if(config.POEM):
            neighbor.poem_distance_scale = (neighbor.poem_distance - poem_min)/(poem_max - poem_min)
            sum_distance = sum_distance + neighbor.poem_distance_scale
        
        if(config.COLOR_POEM):
            neighbor.color_poem_distance_scale = (neighbor.color_poem_distance - color_poem_min)/(color_poem_max - color_poem_min)
            sum_distance = sum_distance + neighbor.color_poem_distance_scale

        if(config.HAAR):
            neighbor.haar_distance_scale = (neighbor.haar_distance - haar_min)/(haar_max - haar_min)
            sum_distance = sum_distance + neighbor.haar_distance_scale
        
        if(config.HAARQ):
            neighbor.haarq_distance_scale = (neighbor.haarq_distance - haarq_min)/(haarq_max - haarq_min)
            sum_distance = sum_distance + neighbor.haarq_distance_scale
        #print item.hsv_distance_scale
        
        #spocteni JEC - zkombinovani priznaku
        neighbor.jec = sum_distance / n
        #print item.jec
        
        if(neighbor.jec > 1):
            print ('lab', lab_min, lab_max, neighbor.lab_distance,neighbor.lab_distance_scale)
            print neighbor.jec
            exit()
            
        if(neighbor.jec < 0):
            print ('lab', lab_min, lab_max, neighbor.lab_distance,neighbor.lab_distance_scale)
            print neighbor.hsv_distance
            print neighbor.rgb_distance
            print neighbor.jec
            exit()
        

#kvůli sortování
def getKey(item):
    return item[1]

  
##############################################################################

train_data = class_pictures.importDataFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDataFromFile(config.DATAFILE_TEST)

#train_data2 = class_pictures.importDataFromFile(config.DATAFILE_TRAIN2)
#
#for data in train_data2:
#    train_data.append(data)


######### spocitani vzdalenosti
for item in test_data:
    count_distance(train_data, item)
    #print item.neighbors[0].jec
    print "--------dalsi test_image --------"

print "----------------"



label_transfer.label_transfer_main(train_data, test_data)

exit()



#tady je problem s tim ze pickle umi jen to zakladni neumi exportovat objekt v objektu (tridu ve tride), takze proto to nepouzivame
#class_pictures.exportDataToFile(test_data, config.DATEFILE_TEST_NEIGHBORS)