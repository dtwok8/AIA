# -*- coding: utf-8 -*-
"""
Presune klicova slova na zaklade JEC metody. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np

#moje
import class_pictures
import class_neighbor
import config


def label_transfer(test_image):
    assigned_keywords = [] # klicova slova, ktera budou nakonec prirazena
    total_count_keywords = 0 # celkovy pocet klicovych slov od sousedu, i s redundantnim zaznamy
    frequence_keywords = {}
    
    
    for i in range(config.COUNT_NEIGHBORS):
        for word in test_image.nereast_neighbors[i][0].picture.keywords:
            if(word in frequence_keywords):
                frequence_keywords[word] += 1
            else:
               frequence_keywords[word] = 1 
            #print word
            total_count_keywords += 1
    
    th = 1.0 / (len(frequence_keywords)-1) #threshold - prah
    
    for word in frequence_keywords.items():
        #print (word[1] / float(total_count_keywords)),">" ,th ,(word[1] / float(total_count_keywords)) > th 
        if((word[1] / float(total_count_keywords)) > th):
            assigned_keywords.append(word[0])
            
    test_image.our_assignment_keywords=assigned_keywords

#/* Assigns variable count of labels to the given image */ 
#QStringList IAPR::assignLabels(QMap<float, QString>& distances, QMap<QString, QStringList>& train_annotations, Params params) { 
#    QStringList list; 
#    //qDebug() << "assigning labels var, train set size " << 
#    distances.size();  #
#    QList<float> keys = distances.keys(); 
#    qSort(keys.begin(), keys.end()); 
#
#    //qDebug() << "Keys size: " << keys.size(); 
#    //qDebug() << train_annotations.keys()[0]; 
#
#    QMap<QString, int> freqs; 
#    int total = 0; 
#    for (int i = 0; i < params.neighbours; i++) { #parames. neigborus je podle mě počet sousedů
#        //qDebug() << distances[keys[i]];  # no tak tohle vypíše vzdálenost ne 
#        foreach(QString s, train_annotations[distances[keys[i]]]) { 
#            //qDebug() << s; 
#            if(freqs.contains(s)) { 
#                freqs[s] += 1; 
#            } 
#            else { 
#                freqs.insert(s, 1); 
#            } 
#            total++; 
#        } 
#    } 
#
#    float th = 1.0 / (freqs.size() - 1);  #prah
#
#    foreach(QString label, freqs.keys()) { 
#        //cout << label.toLatin1().data() << " " << (float)freqs[label] 
#        / total << endl; 
#        if (((float)freqs[label] / total) > th) { 
#            list << label; 
#        } 
#    } 
#
#    return list; 
#} 

 
def write_img_with_keyword_to_txt_file(test_data):
    soubor = open(config.PICTURE_RESULT, 'w')
    
    for img in test_data:
        soubor.write("{};{} \n".format(img.name,img.our_assignment_keywords))
        
    soubor.close()

def write_img_with_keyword_h_a_to_txt_file(test_data):
    soubor = open(config.PICTURE_TEST_KEYWORDS, 'w')
    
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
        print item.name
        print item.keywords


    
    
    print "--------------------------------------"
    #print frequency_word_with_other_word_dictionary['building']['column']
    #print frequency_word_with_other_word_dictionary['column']['building']

    ####prirazeni klicovych slov####
    for item in test_data:
        label_transfer(item)
        print item.name
        print item.keywords
        print item.our_assignment_keywords
#        exit()
    
    
    #class_pictures.exportDataToFile(test_data, config.DATAFILE_TEST_WITH_KEYWORDS) 
    write_img_with_keyword_to_txt_file(test_data)
    write_img_with_keyword_h_a_to_txt_file(test_data)