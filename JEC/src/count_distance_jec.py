# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi trenovacima histogramama a testovacima histograma. Naskaluje vysledky na 0-1. Slozi dohromady jednotlive vysledky (JEC)
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np
import math

from operator import attrgetter #sorter

#moje
import my_class.class_pictures as class_pictures
import my_class.class_neighbor as class_neighbor

import config
import label_transfer
import label_transfer_threshold

def count_distance(H1, H2, metric):
    """
        Spocita vzdalenost podle metriky zadane parametrem. Pri nerozpoznane metrice je vracena L1.
        
        Keyword arguments:
            H1 -- Prvni vektor pro ktery ma byt spoctena vzdalenost. 
            H2 -- Druhy vektor pro ktery ma byt spoctana vzdalenost. 
            metric - metrika.
        Return: 
            distance -- vzdalenost dle dane matriky, pri nerozpoznani metriky je defaultne vracena L1.
    """   
    if(metric == "L1"):
        distance = cv2.norm(H1, H2, cv2.NORM_L1)
        return distance
    
    if(metric == "L2"):
        distance = cv2.norm(H1, H2, cv2.NORM_L2)
        return distance
        
    if(metric == "KL"):
        distance = cv2.compareHist(H1, H2, cv2.HISTCMP_KL_DIV)
        return distance
    
    print "Metrika nebyla rozpoznána! Nastavuji defaulní L1."
    return cv2.norm(H1, H2, cv2.NORM_L1)


def count_all_distance(train_data, test_image):
    """
        Projde vsechny obrazky z trenovaci sady a spocita vzdalenost s testovanym obrazkem.
        Nejprve spocte vzdalenost soucasne zjistuje nejvetsi a nejmensi hodnotu pro dany deskritor, coz bude pouzito u skalovani.
        Zavola si metodu pro spocteni celkove jec vzdalenosti. 
        A nakonec ulozi sousedy serazene podle vzdalenosti k testovanemu obrazku.
        
        Keyword arguments:
            train_data -- Trenovaci sada. 
            test_image -- Testovany obrazek.
            
    """    
    
    print ("distance {}").format(test_image.name)
    #potrebujeme zjistit rozsahy kvuli skalovatelnosti, sice je to neprehledne ale usetrime si dalsi tri cykly
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
            pom_neighbor.rgb_distance = count_distance(picture.rgb, test_image.rgb, config.RGB_DISTANCE)
            if(pom_neighbor.rgb_distance < rgb_min):
                rgb_min = pom_neighbor.rgb_distance
            if(pom_neighbor.rgb_distance > rgb_max):
                rgb_max = pom_neighbor.rgb_distance
        
        if(config.LAB):
            pom_neighbor.lab_distance  = count_distance(picture.lab, test_image.lab, config.LAB_DISTANCE) #kl(picture.lab, test_image.lab)#            
            if(pom_neighbor.lab_distance < lab_min):
                lab_min = pom_neighbor.lab_distance
            if(pom_neighbor.lab_distance > lab_max):
                lab_max = pom_neighbor.lab_distance        
        
        if(config.HSV):
            pom_neighbor.hsv_distance = count_distance(picture.hsv, test_image.hsv, config.HSV_DISTANCE)
            if(pom_neighbor.hsv_distance < hsv_min):
                hsv_min = pom_neighbor.hsv_distance
            if(pom_neighbor.hsv_distance > hsv_max):
                hsv_max = pom_neighbor.hsv_distance
        
        if(config.GABOR):
            pom_neighbor.gabor_distance = count_distance(picture.gabor, test_image.gabor, config.GABOR_DISTANCE)
            if(pom_neighbor.gabor_distance < gabor_min):
                gabor_min = pom_neighbor.gabor_distance
            if(pom_neighbor.gabor_distance > gabor_max):
                gabor_max = pom_neighbor.gabor_distance 
                
        if(config.GABORQ):
            pom_neighbor.gaborq_distance = count_distance(picture.gaborq, test_image.gaborq, config.GABORQ_DISTANCE)
            
            if(pom_neighbor.gaborq_distance < gaborq_min):
                gaborq_min = pom_neighbor.gaborq_distance
            if(pom_neighbor.gaborq_distance > gaborq_max):
                gaborq_max = pom_neighbor.gaborq_distance 
                
        if(config.POEM):            
            pom_neighbor.poem_distance = count_distance(picture.poem, test_image.poem, config.POEM_DISTANCE)
            #om_neighbor.poem_distance = count_distance(picture.poem.astype(np.float32), test_image.poem.astype(np.float32), cv2.HISTCMP_INTERSECT)
            #pom_neighbor.poem_distance = cv2.compareHist(np.zeros(16, dtype=np.float32), np.zeros(16, dtype=np.float32), cv2.HISTCMP_KL_DIV)
            if(pom_neighbor.poem_distance < poem_min):
                poem_min = pom_neighbor.poem_distance
            if(pom_neighbor.poem_distance > poem_max):
                poem_max = pom_neighbor.poem_distance 
        
        if(config.COLOR_POEM):
            pom_neighbor.color_poem_distance = count_distance(picture.color_poem, test_image.color_poem, config.COLOR_POEM_DISTANCE)
            if(pom_neighbor.color_poem_distance < color_poem_min):
                color_poem_min = pom_neighbor.color_poem_distance
            if(pom_neighbor.color_poem_distance > color_poem_max):
                color_poem_max = pom_neighbor.color_poem_distance     
        
        if(config.HAAR):
            pom_neighbor.haar_distance = count_distance(picture.haar, test_image.haar, config.HAAR_DISTANCE)
            if(pom_neighbor.haar_distance < haar_min):
                haar_min = pom_neighbor.haar_distance
            if(pom_neighbor.haar_distance > haar_max):
                haar_max = pom_neighbor.haar_distance 

        if(config.HAARQ):
            pom_neighbor.haarq_distance = count_distance(picture.haarq, test_image.haarq, config.HAARQ_DISTANCE)
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
    """
        Spocita N pro JEC.
        
        Keyword arguments:
            train_data -- Trenovaci sada. 
            test_image -- Testovany obrazek.
        Return:
            n -- spocitane N (pocet priznaku)
    """    
    
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


def count_jec(pom_nei, test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min, gabor_max, gabor_min, gaborq_max, gaborq_min, poem_max, poem_min, color_poem_max, color_poem_min, haar_max, haar_min, haarq_max, haarq_min):
    """
        Naskaluje vzdalenosti a spocita JEC pro prislusny obrazek.
        
        Keyword arguments:
            pom_nei -- Pomocna promena sousedu.
            *_max -- Maximalni hodnta pro tento priznak.
            *_min -- Minimalni hodnota pro tento priznak.
            test_image -- Testovany obrazek.
            
    """    
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
        
        #spocteni JEC - zkombinovani priznaku
        neighbor.jec = sum_distance / n
        

#kvůli sortování
def getKey(item):
    return item[1]

  
##############################################################################

train_data = class_pictures.importDataFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDataFromFile(config.DATAFILE_TEST)

#pomucka kdyz mame malo RAM
#train_data2 = class_pictures.importDataFromFile(config.DATAFILE_TRAIN2)
#
#for data in train_data2:
#    train_data.append(data)


######### spocitani vzdalenosti
for item in test_data:
    count_all_distance(train_data, item)


#zavolani label transfer
if(config.LABEL_TRANSFER == "TH"):
    label_transfer_threshold.label_transfer_main(train_data, test_data)
else:
    label_transfer.label_transfer_main(train_data, test_data)



#tady je problem s tim ze pickle umi jen to zakladni neumi exportovat objekt v objektu (tridu ve tride), takze proto to nepouzivame
#class_pictures.exportDataToFile(test_data, config.DATEFILE_TEST_NEIGHBORS)