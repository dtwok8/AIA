# -*- coding: utf-8 -*-
"""
Presune klicova slova na zaklade JEC metody. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np

#moje
import my_class.class_pictures as class_pictures
import my_class.class_neighbor as class_neighbor

import config


#kvůli sortování
def getKey(item):
    return item[1]

#preneseni klicovych slov
def label_transfer(test_image, train_keywords_dictionary, frequency_word_with_other_word_dictionary):
    """
        Preneseni klicovych slov. Vezme klicova N (dle configu) klicovych slov od prvniho nejblizsiho souseda. Pokud klicovych slov neni dost doplni si je od zbyvajich K-1 nejbylizsich sousedu. 
        
        Keyword arguments:
            test_image -- obrazek ke kteremu se maji klicova slova prenest. 
            train_keywords_dictionary -- slovnik klicovych slov i s jejich vyskyty v trenovaci sade.  
            frequency_word_with_other_word_dictionary - predpocitana frequence slov mezi sebou.
    """ 
    n_keywords={}
    test_image.our_assignment_keywords=[]
   
    #serad klicova slova v I1 podle jejich frekvence v trenovacich datech
    #nereast_neighbors[0] - instance neigbors jako takova, nereast_neighbors[1] - vzdalenost , kvuli serazeni
    for word in test_image.nereast_neighbors[0][0].picture.keywords:
        n_keywords[word] = train_keywords_dictionary[word]        
    
    keywords_list = n_keywords.items() # prevedeni na seznam
    keywords_list = sorted(keywords_list, key=getKey, reverse=True)
    
    if(len(keywords_list) == config.COUNT_KEYWORDS): #zjistit jestli od prvniho mame dostatek klicovych slov
        #test_image.our_assignment_keywords = keywords_list
        for key in keywords_list:
            test_image.our_assignment_keywords.append(key[0])
        return
    
    if(len(keywords_list) > config.COUNT_KEYWORDS):
        #test_image.our_assignment_keywords = keywords_list[0:config.COUNT_KEYWORDS] #usekneme
        for key in keywords_list[0:config.COUNT_KEYWORDS]:
            test_image.our_assignment_keywords.append(key[0]) 
        return
    
    test_image.our_assignment_keywords = keywords_list
    #mame malo klicovych slov proto jeste musime pridat klicovy slova od soused
    add_keywords_from_neighbors(test_image, train_keywords_dictionary, frequency_word_with_other_word_dictionary, n_keywords, keywords_list)

#mame malo klicovych slov proto jeste musime pridat klicovy slova od sousedu
#neni tam naimplementovana lokalni frequnce, ale pri takovem mnozstvi obrazku je mala pravdepodobnost ze se na hrane potkaji dve stejna cisla
def add_keywords_from_neighbors(test_image, train_keywords_dictionary, frequency_word_with_other_word_dictionary, n_keywords, keywords_list):
    """
        Mame malo klicovych slov proto je musime doplnit klicovymi slovy od zbyvajich K-1 nejblizsich sousedu. 
        
        Keyword arguments:
            test_image -- obrazek ke kteremu se maji klicova slova prenest. 
            train_keywords_dictionary -- slovnik klicovych slov i s jejich vyskyty v trenovaci sade.  
            frequency_word_with_other_word_dictionary - predpocitana frequence slov mezi sebou.
            n_keywords -- slovnich prenesenych klicovych slov
            keywords_list --list klicovych slov ktery bude prenesen.
    """ 
    keywords_from_neigbords = {}
    keywords_from_neigbords_local_frequency = {}
    
    #spocitame vyskyty v trenovacich datech s klicovymy slovy prenesenych v kroku 2
    #takze vezmeme vsechny klicovy slova od I2 az Ik
    for img in test_image.nereast_neighbors:
        for word in img[0].picture.keywords:
            if((word in keywords_from_neigbords) == False): #potrebujeme prazdny slovnik vsech slov, budeme posleze vyplnovat frequency v trenovacich datech s jiz frequenci klicovych slov kterou mame od prvniho obrazku    
                keywords_from_neigbords[word] = 0
                keywords_from_neigbords_local_frequency[word] = 1
            else:
                keywords_from_neigbords_local_frequency[word] = keywords_from_neigbords_local_frequency[word] + 1
    
    #co výskyt v trénovacích datech s klicovymy slovy s prenesenych v kroku 2
    for key1, value1 in n_keywords.items():                
        for key2, value2 in keywords_from_neigbords.items():
            if(key2 in frequency_word_with_other_word_dictionary[key1]):
                keywords_from_neigbords[key2] = keywords_from_neigbords[key2]+frequency_word_with_other_word_dictionary[key1][key2] 
    

    keywords_from_neigbords_sorted = sorted(keywords_from_neigbords.items(), key=getKey, reverse=True)
    
    #test_image.our_assignment_keywords = keywords_list
    test_image.our_assignment_keywords=[]
    for key in keywords_list:
        #print key[0]
        test_image.our_assignment_keywords.append(key[0])
    
    
    for item in keywords_from_neigbords_sorted:
        if((item in test_image.our_assignment_keywords) == False):
            test_image.our_assignment_keywords.append(item[0])
  
            if(len(test_image.our_assignment_keywords) >= config.COUNT_KEYWORDS):
                break


def count_keyword_frequency_train_set(train_data):
    """
        Spocita cetnost slov v trenovacich datech a seradi ve slovniku. 
        
        Keyword arguments:
            train_data -- trenovaci data.
        Return:
            keywords_dictionary -- slovnik klicovych slov z trenovaci sady i s jejich frekvenci vyskytu.
    """ 
    keywords_dictionary={}

    for picture in train_data:
        for word in picture.keywords:
            if(word in keywords_dictionary):
                keywords_dictionary[word] = keywords_dictionary[word]+1
            else:
                 keywords_dictionary[word] = 1
    
    return keywords_dictionary  


def frequency_word_with_other_word(train_data):
    """
        Spocte frequance vyskytu s ostatnimy slovy. 
        
        Keyword arguments:
            train_data -- trenovaci data.
        Return:
           dictionary -- slovnik klicovych slov z trenovaci sady i s jejich frekvenci vyskytu s ostanimi slovy z trenovaci sady..
    """ 
    dictionary ={}
    
    for picture in train_data:
        for keyword in picture.keywords:
            if((keyword in dictionary) == False):    
                dictionary[keyword] = {}
    
    
    for key, value in dictionary.items():
        for picture in train_data:
            if(key in picture.keywords): #kdyz je to klicovy slovo v tomhle v kontakru tak ++
                #tak potrebujeme pridat++ ke kazdymu slovu se kterym je v kontaktu
                for keyword in picture.keywords:
                    if(keyword == key):
                        dictionary[key][keyword]=0
                    else:
                        if(keyword in dictionary[key]):
                            dictionary[key][keyword]=dictionary[key][keyword]+1
                        else:
                            dictionary[key][keyword] = 1

     
    return dictionary
 
 
def write_img_with_keyword_to_txt_file(test_data):
    """
        Zapise prenesena klicova slova do souboru. 
        
        Keyword arguments:
            test_data -- list testovacich data
    """ 
    soubor = open(config.PICTURE_RESULT, 'w')
    
    for img in test_data:
        soubor.write("{};{} \n".format(img.name,img.our_assignment_keywords))
        
    soubor.close()


def write_img_with_keyword_h_a_to_txt_file(test_data):
    """
        Zapise vysledek klasifikace do souboru. I s presnosti a uplnosti.
        
        Keyword arguments:
            test_data -- list testovacich data
    """
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
    """
        Hlavni metoda prenaseni klicovych slov.
        
        Keyword arguments:
            train_data -- list trenovacich dat
            test_data -- list testovacich data
    """
    print "label transfer predpocitavam ... "
    #cetnost klicovych slov v trenovacich datech
    train_keywords_dictionary=count_keyword_frequency_train_set(train_data) 
    
    frequency_word_with_other_word_dictionary = frequency_word_with_other_word(train_data)


    ####prirazeni klicovych slov####
    for item in test_data:
        label_transfer(item, train_keywords_dictionary, frequency_word_with_other_word_dictionary)
        print ("label transfer {}").format(item.name)
    

    write_img_with_keyword_to_txt_file(test_data)
    write_img_with_keyword_h_a_to_txt_file(test_data)