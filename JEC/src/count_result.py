# -*- coding: utf-8 -*-
"""
Spocita Precision a recall
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np
import pickle
import sys

#moje
import my_class.class_keywords as class_keywords
import my_class.class_pictures_result as class_pictures
import config
import label_transfer




def getKeywords(train_data):
    """
        Zjisti vsechny slova z trenovaci mnoziny a pro kazde slovo vytvori instanci v keywords_list.
        Pres slovnik je to reseno z duvodu redundance.

        Keyword arguments:
            train_data -- list trenovacich dat (obrazku)
        
    """
    dictionary ={}
    
    for picture in train_data:
        for keyword in picture.keywords:
            if((keyword in dictionary) == False):    
                dictionary[keyword] = 0
    
    keywords_list = []
    for item in dictionary.items():
        keywords_list.append(class_keywords.Keywords(item[0]))
   
    return keywords_list

def count_precsion_recall(list_keywords, test_data):
    """
        Spocita precision a recall pro kazde slovo. 
        
        Keyword arguments:
            list_keywords -- list obsahujici objekty klicova slova
            test_data -- list testovaci dat (obrazku)
    """
    
    collectively_result = {}
    collectively_result['count_nonzero_word'] = 0
    collectively_result['count_keywords'] = len(list_keywords)

    
    count_precision = 0
    count_recall = 0
    
    print len (list_keywords)
    for item in list_keywords:
        w_a = 0
        w_c = 0
        w_h = 0
        

        #print item.keyword
        for picture in test_data:
            #print picture.keywords
            #print picture.our_assignment_keywords
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
            count_precision = count_precision +  item.precision
        if(w_h != 0): 
            item.recall = w_c/float(w_h)
            count_recall = count_recall + item.recall
            

        if(item.recall > 0 and item.precision > 0):
            collectively_result['count_nonzero_word'] = collectively_result['count_nonzero_word'] + 1
            print '{} recall: {} precision: {} {} {} {} '.format(item.keyword, item.recall, item.precision, item.w_auto, item.w_human, item.w_correctly)
    
    collectively_result['precision'] = count_precision / len(list_keywords)
    collectively_result['recall'] = count_recall / len(list_keywords)
    print "Souhrn: nenulových slov {} z {}  precision {} recall {} \n".format(collectively_result['count_nonzero_word'], collectively_result['count_keywords'], collectively_result['precision'], collectively_result['recall'])
    return collectively_result
    
        
def write_keyword_result_to_txt_file(list_keywords, collectively_result):
    soubor = open(config.KEYWORDS_RESULT, 'w')
    
    soubor.write("Souhrn: nenulových slov {} z {}  precision {} recall {} \n".format(collectively_result['count_nonzero_word'], collectively_result['count_keywords'],collectively_result['precision'], collectively_result['recall']))
    
    for word in list_keywords:
        soubor.write("{} - precision: {} recall: {} \n".format(word.keyword, word.precision, word.recall))
        
    soubor.close()

def read_data_from_file():  
    try:
        f = open(config.PICTURE_ALL_KEYWORDS, 'r')
    except: 
        print("Pri nacitani dat do souboru nastala chyba. Zkontrolujte jmeno souboru a zda existuje.")
        sys.exit(1)
        
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

#for item in test_data:
#    print item.name
#    print item.keywords
#    print item.our_assignment_keywords


list_keywords = getKeywords(train_data) #vsechny klicovy slova z trenovacich dat
collectively_result = count_precsion_recall(list_keywords, test_data) #zjistit jestli jsou spravne přiřazený   
write_keyword_result_to_txt_file(list_keywords, collectively_result)