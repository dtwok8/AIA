# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi testovacima histogramama a testovacima histograma. Naskaluje vysledky na 0-1. Slozi dohromady jednotlive vysledky (JEC)
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np
from Queue import PriorityQueue

#moje
import class_pictures
import class_neighbor
import config


#kvůli sortování
def getKey(item):
    return item[1]

#preneseni klicovych slov
def label_transfer(test_image, train_keywords_dictionary):
    print "-------------------------------------------"
    n_keywords={}
   
    #serad klicova slova v I1 podle jejich frekvence v trenovacich datech
    for word in test_image.nereast_neighbors[0][0].picture.keywords:
        n_keywords[word] = train_keywords_dictionary[word]        
    
    keywords_list = n_keywords.items() # prevedeni na seznam
    keywords_list = sorted(keywords_list, key=getKey, reverse=True)
    print keywords_list
    
    if(len(keywords_list) > config.COUNT_NEIGHBORS): #zjistit jestli od prvniho mame dostatek klicovych slov
        return
    #else:
        #takze vezmeme vsechny klicovy slova od I2 az Ik
        #
    
    #pokud ne pokracujeme dale
    #seradime klicova slova od I2 do Ik podle dvou faktorů
            #1) co výskyt v trénovacích datech s klicovymy slovy s prenesenych v kroku 2
            #2) localni frequnce (jak casto se objevuji u I2 az Ik)
            # vyberte největši n-|I1| klicovych slov prenesnych


#spocita cetnost slov v trenovacich datech a seradi ve slovniku 
def count_keyword_frequency_train_set(train_data): 
    keywords_dictionary={}

    for picture in train_data:
        for word in picture.keywords:
            if(word in keywords_dictionary):
                keywords_dictionary[word] = keywords_dictionary[word]+1
            else:
                 keywords_dictionary[word] = 1
    
    return keywords_dictionary  

def label_transfer_main(train_data, test_data):
    #cetnost klicovych slov v trenovacich datech
    train_keywords_dictionary=count_keyword_frequency_train_set(train_data) 

    ####prirazeni klicovych slov####
    for item in test_data:
        label_transfer(item, train_keywords_dictionary)