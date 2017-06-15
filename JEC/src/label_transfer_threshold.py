# -*- coding: utf-8 -*-
"""
Presune klicova slova na zaklade dynamickeho preneseni klicovych slov pomoci prahovani. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np

#moje
import my_class.class_pictures as class_pictures
import my_class.class_neighbor as class_neighbor
import config


def label_transfer(test_image):
    assigned_keywords = [] # klicova slova, ktera budou nakonec prirazena
    total_count_keywords = 0 # celkovy pocet klicovych slov od sousedu, i s redundantnim zaznamy
    frequence_keywords = {}
    
    
    for i in range(config.COUNT_NEIGHBORS):
        for word in test_image.nereast_neighbors[i][0].picture.keywords:
            print test_image.nereast_neighbors[i][0].picture.name
            if(word in frequence_keywords):
                frequence_keywords[word] += 1
            else:
               frequence_keywords[word] = 1 
            #print word
            total_count_keywords += 1
    
    if(len(frequence_keywords) == 1):
        word = frequence_keywords.items()
        assigned_keywords.append(word[0][0])
        test_image.our_assignment_keywords = assigned_keywords
        return 
        
    th = 1.0 / (len(frequence_keywords)-1) #threshold - prah
    
    for word in frequence_keywords.items():
        #print (word[1] / float(total_count_keywords)),">" ,th ,(word[1] / float(total_count_keywords)) > th 
        if((word[1] / float(total_count_keywords)) > th):
            assigned_keywords.append(word[0])
            
    test_image.our_assignment_keywords=assigned_keywords
    
 
def write_img_with_keyword_to_txt_file(test_data):
    soubor = open(config.PICTURE_RESULT, 'w')
    
    for img in test_data:
        soubor.write("{};{} \n".format(img.name,img.our_assignment_keywords))
        
    soubor.close()


def write_img_with_keyword_h_a_to_txt_file(test_data):
    soubor = open(config.PICTURE_ALL_KEYWORDS, 'w')
    
    for img in test_data:
        string_humain_keyword = ""
        string_automatic_keyword = ""
        
        for word in img.keywords:
            string_humain_keyword = string_humain_keyword + " "+word 
     
        for word in img.our_assignment_keywords:
            string_automatic_keyword = string_automatic_keyword + " "+word 
        
        soubor.write("{};{};{} \n".format(img.name, string_humain_keyword, string_automatic_keyword))
        
    soubor.close()


def label_transfer_main(train_data, test_data):
    for item in test_data:
        label_transfer(item)
        print item.name
        #print item.keywords
        #print item.our_assignment_keywords
#        exit()
    
    
    #class_pictures.exportDataToFile(test_data, config.DATAFILE_TEST_WITH_KEYWORDS) 
    write_img_with_keyword_to_txt_file(test_data)
    write_img_with_keyword_h_a_to_txt_file(test_data)