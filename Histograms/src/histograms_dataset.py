# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:02:46 2016

@author: lada
"""

import cv2
import numpy as np
#import sys
#import re
#import os.path
#import poem
#from scipy.spatial import distance

#train_list = "/media/lada/Data/image_labelling_datasets/iaprtc12.20091111/iaprtc12_train_list.txt"
test_list = "/media/lada/Data/image_labelling_datasets/iaprtc12.20091111/iaprtc12_test_list.txt"
data_dir = "/media/lada/Data/image_labelling_datasets/iaprtc12/images"
annot_dir = "/media/lada/Data/image_labelling_datasets/iaprtc12/annotations_complete_eng"
annot_alt = "/media/lada/Data/image_labelling_datasets/iaprtc12/annotations"
dictionary_path = "/media/lada/Data/image_labelling_datasets/iaprtc12.20091111/iaprtc12_dictionary.txt"


def prepare_annotations():  
    print "pakarna"
    f = open("../lists_data_path/iapr_train.txt", 'r')
  
    #f = open(train_list, 'r')
    for line in f:
        print line
#    if os.path.exists(annot_dir + "/" + line.strip() + ".eng"):
#      ff = open(annot_dir + "/" + line.strip() + ".eng", 'r')
#    else:
#      ff = open(annot_alt + "/" + line.strip() + ".eng", 'r')
    #str = ""
#    for l in ff:
#      if "<DESCRIPTION>" in l:
#        str = l.strip()      
#        
#    ff.close()
#    g.write(data_dir + "/" + line.strip() + ".jpg;")
#    for word in dictionary:
#      #print word
#      if word in str:
#        #print word, dictionary[word]     
#        g.write(word + " ")
#    g.write("\n")  
    
    f.close()
    #g.close()
  
#  g = open("iapr_test.txt", 'w')
#  f = open(test_list, 'r')
#  for line in f:
#    if os.path.exists(annot_dir + "/" + line.strip() + ".eng"):
#      ff = open(annot_dir + "/" + line.strip() + ".eng", 'r')
#    else:
#      ff = open(annot_alt + "/" + line.strip() + ".eng", 'r')
#    #str = ""
#    for l in ff:
#      if "<DESCRIPTION>" in l:
#        str = l.strip()      
#        
#    ff.close()
#    g.write(data_dir + "/" + line.strip() + ".jpg;")
#    for word in dictionary:
#      #print word
#      if word in str:
#        #print word, dictionary[word]     
#        g.write(word + " ")
#    g.write("\n")  
#    
#  f.close()
#  g.close()
prepare_annotations()