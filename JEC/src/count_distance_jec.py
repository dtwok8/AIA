# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi testovacima histogramama a testovacima histograma. Naskaluje vysledky na 0-1. Slozi dohromady jednotlive vysledky (JEC)
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np

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
    print ( rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)
    print ( rgb_max , rgb_min, lab_max > 3333.72839, lab_min, hsv_max, hsv_min)
    test_image.neighbors  = []
    #spocitame vzdalenosti mezi testovacim obrazkem a tranovaci mnozinou
    #zaroven spocitame minmum a maximum pro dany testovaci obrazek
    for picture in train_data:
        pom_neighbor = class_neighbor.Neighbor(picture)
        pom_neighbor.rgb_distance = cv2.norm(picture.lab, test_image.lab, cv2.NORM_L1)
        if(pom_neighbor.rgb_distance < rgb_min):
            rgb_min = pom_neighbor.rgb_distance
        if(pom_neighbor.rgb_distance > rgb_max):
            rgb_max = pom_neighbor.rgb_distance
        
        pom_neighbor.lab_distance  = cv2.compareHist(picture.lab, test_image.lab, cv2.HISTCMP_KL_DIV)            
        if(pom_neighbor.lab_distance < lab_min):
            lab_min = pom_neighbor.lab_distance
        if(pom_neighbor.lab_distance > lab_max):
            lab_max = pom_neighbor.lab_distance        
        
        pom_neighbor.hsv_distance = cv2.norm(picture.hsv, test_image.hsv, cv2.NORM_L1)
        if(pom_neighbor.hsv_distance < hsv_min):
            hsv_min = pom_neighbor.hsv_distance
        if(pom_neighbor.hsv_distance > hsv_max):
            hsv_max = pom_neighbor.hsv_distance
        
        test_image.neighbors.append(pom_neighbor) #pridani souseda

    count_jec_n_3(test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)   

#spocita JEC pro tri parametry rgb, hsv, lab, ty to musíš naškálovat od 0 o 1 takže asi ten jec můžeš počítat stejně až budeš mít všechny ty výsledky
def count_jec_n_3(test_image, rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min):
    print ( rgb_max, rgb_min, lab_max, lab_min, hsv_max, hsv_min)
    for neighbor in test_image.neighbors:
        #naskalovani na 0 - 1
        neighbor.rgb_distance_scale = ((neighbor.rgb_distance-rgb_min)/((rgb_max - rgb_min)/100 ))/100
        #print item.rgb_distance_scale
        
        neighbor.lab_distance_scale = ((neighbor.lab_distance-lab_min)/((lab_max - lab_min)/100 ))/100 
        #print ('lab', lab_min, lab_max, item.lab_distance,item.lab_distance_scale)
        
        neighbor.hsv_distance_scale = ((neighbor.hsv_distance-hsv_min)/((hsv_max - hsv_min)/100 ))/100
        #print item.hsv_distance_scale
        
        #spocteni JEC - zkombinovani priznaku
        neighbor.jec = (neighbor.rgb_distance_scale/3) + (neighbor.lab_distance_scale/3) + (neighbor.hsv_distance_scale/3)
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
        
################################### label transfer ##########################    
#    keywords_list = keywords_dictionary.items() # prevedeni na seznam
#    
#    print keywords_list
#
#    
#    keywords_list = sorted(keywords_list, key=getKey, reverse=True)
#    for item in keywords_list:
#        print (item[0],"-", item[1])
#    #return keywords_dictionary
#    exit()

#kvůli sortování
def getKey(item):
    return item[1]



    
##############################################################################

train_data = class_pictures.importDataFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDataFromFile(config.DATAFILE_TEST)


######### spocitani vzdalenosti
for item in test_data:
    count_distance(train_data, item)
    print item.neighbors[0].jec
    print "--------dalsi test_image --------"

print "----------------"

######## serazeni sousedu podle jejich vzdalenosti
for item in test_data: #tenhle cyklus si muzu usetrit
    keywords_prepare_sort=[]
    for neighbor in item.neighbors:
        keywords_prepare_sort.append([neighbor, neighbor.jec]) 
    
    item.nereast_neighbors = sorted(keywords_prepare_sort, key=getKey, reverse=True)

############



label_transfer.label_transfer_main(train_data, test_data)

exit()



#tady je problem s tim ze pickle umi jen to zakladni neumi exportovat objekt v objektu (tridu ve tride)
class_pictures.exportDataToFile(test_data, config.DATEFILE_TEST_NEIGHBORS)