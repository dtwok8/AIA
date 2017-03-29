# -*- coding: utf-8 -*-
"""
Spocita Precision a recall
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np

#moje
import class_pictures
import class_neighbor
import class_keywords
import config
import label_transfer


def getKeywords(train_data):
    dictionary ={}
    
    for picture in train_data:
        for keyword in picture.keywords:
            if((keyword in dictionary) == False):    
                dictionary[keyword] = {}
    
    keywords_list = []
    for item in dictionary.items():
        keywords_list.append(class_keywords.Keywords(item[0]))
   
    return keywords_list




train_data = class_pictures.importDataFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDataFromFile(config.DATAFILE_TEST_WITH_KEYWORDS)

list_keywords = getKeywords(train_data)

for item in list_keywords:
    w_a = 0
    w_c = 0
    w_h = 0
    
    #print item.keyword
    for picture in test_data:
        #print picture.keywords
        #print picture.our_assignment_keywords
        if (item.keyword in picture.keywords[0]):
            w_h = w_h + 1
            #print "wh"
        if (item.keyword in picture.our_assignment_keywords[0]):
            w_a = w_a + 1
            #print "w_a"
        if((item.keyword in picture.keywords[0]) and (item.keyword in picture.our_assignment_keywords[0])):
            w_c = w_c + 1
            #print "w_c"
    
    if(w_a != 0): 
        item.precision = w_c/w_a
    if(w_h != 0): 
        item.recall = w_c/w_h
        
    print '{} recall: {} precision{}'.format(item.keyword, item.recall, item.precision)

    

#vsechny klicovy slova
#zjistit jestli jsou spravne přiřazený