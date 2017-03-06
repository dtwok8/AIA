# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""
#btw zaloz si work playlist, a pridej si tam ty monstra písničky, při nich se pracuje docela dobře, nacey own it prostě ta pisnička z twl hraje tam Bianca 
#to mi tak napadlo jak si chces ulozit ty histogramy a k tomu cestu k obrázku aklíčový slova, 
#i když teoreticky me by stacilo jen histogramy a klicovy slova
# mo

import cv2
import numpy as np

#moje
import class_pictures

#import sys
#import re
#import os.path
#import poem
#from scipy.spatial import distance

#train_list = "../Data/image_labelling_datasets/iaprtc12/iapr_train_list.txt"
train_list = "../../Data/image_labelling_datasets/iaprtc12/iapr_train_list2.txt"
test_list = "/media/lada/Data/image_labelling_datasets/iaprtc12.20091111/iaprtc12_test_list.txt"
data_dir = "/media/lada/Data/image_labelling_datasets/iaprtc12/images"
annot_dir = "/media/lada/Data/image_labelling_datasets/iaprtc12/annotations_complete_eng"
annot_alt = "/media/lada/Data/image_labelling_datasets/iaprtc12/annotations"
dictionary_path = "/media/lada/Data/image_labelling_datasets/iaprtc12.20091111/iaprtc12_dictionary.txt"

def prepare_annotations():  
    f = open(train_list, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova, vis ze tohle ti taky bude fungovat jen u nekterych dat, protoze nektery tam maji ty xml soubory
        print type(split_line)
        print split_line[0]
        img = cv2.imread(split_line[0])
        
        cv2.imshow('P201302280779501',img)        
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        x.rgb = countRGBHistogram(img)
        x.lab = countLABHistogram(img)
        x.hsv = countHSVHistogram(img)
        

        
        print x.keywords
        print x.keywords[0]
        
       
    
    
        listPictures.append(x)
        
        print type(x.rgb[0])
        print x.rgb[0]
        print x.lab[0]
        print x.hsv[0]
        
        
        #lab = countLABHistogram(img)
        #hsv = countHSVHistogram(img)
        #print type(img)
        
        #TODO asi spočítat vzdálenosti mezi jednotlivýma histogramama, načíst to do nějakýho souboru, ale aby se to dalo snadno kontrolovat takže asi na 
        #to napsat metodu přímo k tomu class_pictures, jako načti data ze souboru a načti data do souboru, tam by se měla dát přidat "statická metoda ne?"
        #souvisí to s tím v podstatě.. 
        
        #countHistogram(img); #hmm.. jak to tý metody pošlu ten obrázek?, teoreticky tam můžu poslat string, a otevřít si to až v tý metodě,
        #ale na to by zase chtěla jiná metoda, aby se rovnou kontrolovalo jestli ten soubor 
        #takže nejlepší by asi bylo udělat metodu na otevření toho obrázku, + kontrola jestli exsituje, 
        #což mi připomíná že tahle metoda je pojmenovaná dost debilně už nevím co jsem tím názvem uplně zamýšlela.
        #jo a taky by si měla začít řešit ten latech mrknout na šablony a ták

        #print line
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
    
    print "-----------------------------"
    print len(listPictures)
    for member in listPictures:
        print member.name
        print member.rgb[0]
    
    print "vzdálenost: "
    print kl(listPictures[0].rgb, listPictures[1].rgb)
    print kl(listPictures[0].rgb, listPictures[2].rgb)
    print kl(listPictures[0].rgb, listPictures[3].rgb)
    print kl(listPictures[1].rgb, listPictures[3].rgb)
    #print kl(listPictures[0].lab, listPictures[1].lab) #blba nula ve vektoru, navíc to je asi stejně blbě ty tam posíláš 2 trojrozměrný vektory


    #cv2.compareHist(np.asarray(listPictures[0].rgb),np.asarray(listPictures[1].rgb), cv2.HISTCMP_CHISQR)
   # help(cv2)
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
    class_pictures.exportDataToFile(listPictures)
    x = class_pictures.importDateFromFile()
    print x[0].rgb
    


def countRGBHistogram(img):
    list_rgb=[0,0,0]
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print ("------RGB--------")
    print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))

    for i in (0,1,2):
        for x in range(len(img)):
            for y in range(len(img[x])):
                value = img.item(x,y,i) 
                index = value/16
                list[index]=list[index]+1
        print list
        list_rgb[i] = list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_rgb

def countLABHistogram(img):
    print ("------LAB--------")
    #prevedeni na LAB
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    print "shape: "
    print lab_image.shape
    print "amin: {}, amax: {}".format(np.amin(lab_image), np.amax(lab_image))
    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(lab_image[:,:,0]),np.amax(lab_image[:,:,0]),np.amin(lab_image[:,:,1]), np.amax(lab_image[:,:,1]), np.amin(lab_image[:,:,2]), np.amax(lab_image[:,:,1]))
    #l_channel,a_channel,b_channel = cv2.split(lab_image)
    #lab = cv2.split(lab_image)

    list_LAB=[0,0,0]
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for i in (0,1,2):
        for x in range(len(lab_image)):
            for y in range(len(lab_image[x])):
                value = lab_image.item(x,y,i)
                index = value/16
                list[index]=list[index]+1
        print list
        list_LAB[i]=list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    return list_LAB

def countHSVHistogram(img):
    print ("------HSV--------")
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    print "amin: {}, amax: {}".format(np.amin(hsv_image), np.amax(hsv_image))
    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(hsv_image[:,:,0]),np.amax(hsv_image[:,:,0]),np.amin(hsv_image[:,:,1]), np.amax(hsv_image[:,:,1]), np.amin(hsv_image[:,:,2]), np.amax(hsv_image[:,:,1]))

    print hsv_image.shape
    #hsv = cv2.split(hsv_image)
    list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    list_hsv=[0,0,0]

    for i in (0,1,2):
        for x in range(len(hsv_image)):
            for y in range(len(hsv_image[x])):
                value = hsv_image.item(x,y,i) 
                index = value/16
                list[index]=list[index]+1
        print list 
        list_hsv[i]=list
        list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print len(hsv_image[0])
    print len(hsv_image[0][0])
    print type(hsv_image)
    return list_hsv

def kl(p, q):
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def L1(v1, v2):
    if(len(v1)!=len(v2)):
        print "error"
        return -1
    return sum([abs(v1[i]-v2[i]) for i in range(len(v1))])

prepare_annotations()