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

def count_precsion_recall(list_keywords, test_data):
    print len (list_keywords)
    for item in list_keywords:
        w_a = 0
        w_c = 0
        w_h = 0

        #print item.keyword
        for picture in test_data:
            #print picture.keywords
            #print picture.our_assignment_keywords
            # uz vim kde je chyba prave v tom ze tam je [klicovy slovo][pocet]
            if (item.keyword in picture.keywords):
                w_h = w_h + 1
                #print "wh"
            if (item.keyword in picture.our_assignment_keywords):
                w_a = w_a + 1
                #print "w_a"
            if((item.keyword in picture.keywords) and (item.keyword in picture.our_assignment_keywords)):
                w_c = w_c + 1
                #print "w_c"
                
  
                
        item.w_auto = w_a
        item.w_human = w_h
        item.w_correctly = w_c
        
        if(w_a != 0): 
            item.precision= w_c/float(w_a)
        if(w_h != 0): 
            item.recall = w_c/float(w_h)

        if(item.recall > 0 and item.precision > 0):
            print '{} recall: {} precision: {} {} {} {} '.format(item.keyword, item.recall, item.precision, item.w_auto, item.w_human, item.w_correctly)
        
def write_keyword_result_to_txt_file(list_keywords):
    soubor = open(config.KEYWORDS_RESULT, 'w')
    
    for word in list_keywords:
        soubor.write("{} - precision: {} recall: {} \n".format(word.keyword, word.precision, word.recall))
        
    soubor.close()

def read_data_from_file():
    f = open(config.PICTURE_TEST_KEYWORDS, 'r')

    listPictures = []

    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print 'test {}'.format(split_line[0])
        img = cv2.imread(split_line[0])      

        x = class_pictures.Pictures(split_line[0], split_line[1], split_line[2])
        listPictures.append(x)
    
    f.close()
    return listPictures
    

train_data = class_pictures.importDataFromFile(config.DATAFILE_TRAIN)
test_data = read_data_from_file()

for item in test_data:
    print item.name
    print item.keywords
    print item.our_assignment_keywords


list_keywords = getKeywords(train_data) #vsechny klicovy slova
count_precsion_recall(list_keywords, test_data) #zjistit jestli jsou spravne přiřazený   
write_keyword_result_to_txt_file(list_keywords)

