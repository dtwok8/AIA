# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi histograma
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 
#to mi tak napadlo jak si chces ulozit ty histogramy a k tomu cestu k obrázku aklíčový slova, 
#i když teoreticky me by stacilo jen histogramy a klicovy slova
# mo

import cv2
import numpy as np

#moje
import class_pictures
import class_neighbor
import config


def count_distance(train_data, test_image):
    #potrebujeme zjistit rozdahy kvuli skalovatelnosti, usetrime si dalsi tri cykly
    rgb_min=float("inf")
    rgb_max=0
    lab_min=float("inf")
    lab_max=0
    hsv_min=float("inf")
    hsv_max=0 
    
    float("inf")
    for item in train_data:
        pom_neighbor = class_neighbor.Neighbor(item)
        pom_neighbor.rgb_distance = cv2.norm(item.lab, test_image.lab, cv2.NORM_L1)
        if(pom_neighbor.rgb_distance < rgb_min):
            rgb_min = pom_neighbor.rgb_distance
        if(pom_neighbor.rgb_distance > rgb_max):
            rgb_max = pom_neighbor.rgb_distance
        
        pom_neighbor.lab_distance  = cv2.compareHist(item.lab, test_image.lab, cv2.HISTCMP_KL_DIV)
        if(pom_neighbor.lab_distance < lab_min):
            lab_min = pom_neighbor.lab_distance
        if(pom_neighbor.lab_distance > lab_max):
            lab_max = pom_neighbor.lab_distance
        
        pom_neighbor.hsv_distance = cv2.norm(item.hsv, test_image.hsv, cv2.NORM_L1)
        if(pom_neighbor.hsv_distance < hsv_min):
            hsv_min = pom_neighbor.hsv_distance
        if(pom_neighbor.lab_distance > hsv_max):
            hsv_max = pom_neighbor.lab_distance
        
        test_image.neighbors.append(pom_neighbor)
    count_jec_n_3(test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)    
#    print "vzdálenost: "
#    print cv2.compareHist(np.array(listPictures[0].rgb, dtype=np.float32),np.array(listPictures[1].rgb, dtype=np.float32), cv2.HISTCMP_CHISQR)
#    print cv2.compareHist(np.array(listPictures[0].rgb, dtype=np.float32),np.array(listPictures[1].rgb, dtype=np.float32), cv2.HISTCMP_KL_DIV)
#    print cv2.compareHist(np.array(listPictures[0].lab, dtype=np.float32),np.array(listPictures[1].lab, dtype=np.float32), cv2.HISTCMP_KL_DIV)


#spocita JEC pro tri parametry rgb, hsv, lab, ty to musíš naškálovat od 0 o 1 takže asi ten jec můžeš počítat stejně až budeš mít všechny ty výsledky
def count_jec_n_3(test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min):

    for item in test_image.neighbors:
        item.rgb_distance_scale = ((item.rgb_distance-rgb_min)/((rgb_max - rgb_min)/100 ))/100
        print item.rgb_distance_scale
        
        item.lab_distance_scale = ((item.lab_distance-lab_min)/((lab_max - lab_min)/100 ))/100 
        print item.lab_distance_scale
        
        item.hsv_distance_scale = ((item.hsv_distance-hsv_min)/((hsv_max - hsv_min)/100 ))/100
        print item.hsv_distance_scale
        
    
    #naskalovani na 0 - 1
#    
#    
#    jec = (neigbor.rgb_distance/3) + (neigbor.lab_distance/3) + (neigbor.hsv_distance/3)
#    return jec

    

#prepare_annotations()

train_data = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDateFromFile(config.DATAFILE_TEST)
count_distance(train_data, test_data[0])

class_neighbor.exportDataToFile(test_data, config.DATEFILE_TEST_NEIGHBORS)