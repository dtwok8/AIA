# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np

#moje
import class_pictures
import config

def prepare_annotations():  
    f = open(config.TRAIN_LIST, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print type(split_line)
        print split_line[0]
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        
        x.rgb = countRGBHistogram(img)
        x.lab = countLABHistogram(img)
        x.hsv = countHSVHistogram(img)
        
        #testovaci vypisy
        print x.keywords
        print x.keywords[0]
        print type(x.rgb[0])
        print x.rgb[0]
        print x.lab[0]
        print x.hsv[0]
        
        listPictures.append(x)
        
        
        #TODO asi spočítat vzdálenosti mezi jednotlivýma histogramama, načíst to do nějakýho souboru, ale aby se to dalo snadno kontrolovat takže asi na 
        #to napsat metodu přímo k tomu class_pictures, jako načti data ze souboru a načti data do souboru, tam by se měla dát přidat "statická metoda ne?"
        #souvisí to s tím v podstatě.. 
        
        #countHistogram(img); #hmm.. jak to tý metody pošlu ten obrázek?, teoreticky tam můžu poslat string, a otevřít si to až v tý metodě,
        #ale na to by zase chtěla jiná metoda, aby se rovnou kontrolovalo jestli ten soubor 
        #takže nejlepší by asi bylo udělat metodu na otevření toho obrázku, + kontrola jestli exsituje, 
        #což mi připomíná že tahle metoda je pojmenovaná dost debilně už nevím co jsem tím názvem uplně zamýšlela.
        #jo a taky by si měla začít řešit ten latech mrknout na šablony a ták
  
    
    f.close()
    class_pictures.exportDataToFile(listPictures, config.DATAFILE_TRAIN)
    
    print "------------Natrenovano-----------------"
#    print len(listPictures)
#    for member in listPictures:
#        print member.name
#        print member.rgb[0]
    
    print "vzdálenost: "
    print cv2.compareHist(np.array(listPictures[0].rgb, dtype=np.float32),np.array(listPictures[1].rgb, dtype=np.float32), cv2.HISTCMP_CHISQR)
    print cv2.compareHist(np.array(listPictures[0].rgb, dtype=np.float32),np.array(listPictures[1].rgb, dtype=np.float32), cv2.HISTCMP_KL_DIV)
    print cv2.compareHist(np.array(listPictures[0].lab, dtype=np.float32),np.array(listPictures[1].lab, dtype=np.float32), cv2.HISTCMP_KL_DIV)
    #print kl(listPictures[0].rgb, listPictures[1].rgb)
    #print kl(listPictures[0].rgb, listPictures[2].rgb)
    #print kl(listPictures[0].rgb, listPictures[3].rgb)
    #print kl(listPictures[1].rgb, listPictures[3].rgb)
    #print kl(listPictures[0].lab, listPictures[1].lab) #blba nula ve vektoru, navíc to je asi stejně blbě ty tam posíláš 2 trojrozměrný vektory

    
    x = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)
    print x[0].rgb

def count_train_histogram():
    f = open(config.TRAIN_LIST, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print type(split_line)
        print split_line[0]
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        #x.rgb = countRGBHistogram(img)
        
       
        asd = countRGBHistogram(img) 
        
        print "-------------sleduj--------------"
        new = np.array(asd, dtype=np.float32)
        x.rgb = np.array(asd, dtype=np.float32)
        print new
        print type(new)
        print "rgb:" 
        print type(asd)
        print asd
        exit()
        
        x.lab = countLABHistogram(img)
        x.hsv = countHSVHistogram(img)
        
        #testovaci vypisy
        print x.keywords
        print x.keywords[0]
        print type(x.rgb[0])
        print x.rgb[0]
        print x.lab[0]
        print x.hsv[0]
        
        listPictures.append(x)
        exit()
    f.close()
    class_pictures.exportDataToFile(listPictures, config.DATAFILE_TRAIN)
    
    x = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)
    print x[0].rgb

def count_test_histogram():
    f = open(config.TEST_LIST, 'r')
    
    listPictures = []
    
    for line in f: 
        split_line = line.split(";") # rozdeli radek na cestu k obrazku a klicova slova 
        print type(split_line)
        print split_line[0]
        img = cv2.imread(split_line[0])      
    
        x = class_pictures.Pictures(split_line[0], split_line[1])
        x.rgb = countRGBHistogram(img)
        x.lab = countLABHistogram(img)
        x.hsv = countHSVHistogram(img)
        
        #testovaci vypisy
        print x.keywords
        print x.keywords[0]
        print type(x.rgb[0])
        print x.rgb[0]
        print x.lab[0]
        print x.hsv[0]
        
        listPictures.append(x)
    
    f.close()
    class_pictures.exportDataToFile(listPictures, config.DATAFILE_TRAIN)
    
    x = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)
    print x[0].rgb

#def countRGBHistogram(img):
#    array_rgb = np.zeros(shape=(3, 16), dtype=float32)
#    array_pom = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] , dtype=float32)
#
#    print ("------RGB--------")
#    print "amin: {}, amax: {}".format(np.amin(img), np.amax(img))
#    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(img[:,:,0]),np.amax(img[:,:,0]),np.amin(img[:,:,1]), np.amax(img[:,:,1]), np.amin(img[:,:,2]), np.amax(img[:,:,1]))
#
#    for i in (0,1,2):
#        for x in range(len(img)):
#            for y in range(len(img[x])):
#                value = img.item(x,y,i) 
#                index = value/16
#                array_pom[index]=array_pom[index]+1
#        print array_pom
#        array_rgb[i] = array_pom
#        array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#        print "format--------------------------------"
#        print type(array_rgb)
#        print type(array_pom)
#    return array_rgb


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

    array_lab = np.zeros(shape=(3, 16))
    array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    for i in (0,1,2):
        for x in range(len(lab_image)):
            for y in range(len(lab_image[x])):
                value = lab_image.item(x,y,i)
                index = value/16
                array_pom[index]=array_pom[index]+1
        print array_pom
        array_lab[i]=array_pom
        array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    return array_lab

def countHSVHistogram(img):
    print ("------HSV--------")
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    print "amin: {}, amax: {}".format(np.amin(hsv_image), np.amax(hsv_image))
    print "1: {} - {}, 2: {} - {}, 3: {} - {}".format(np.amin(hsv_image[:,:,0]),np.amax(hsv_image[:,:,0]),np.amin(hsv_image[:,:,1]), np.amax(hsv_image[:,:,1]), np.amin(hsv_image[:,:,2]), np.amax(hsv_image[:,:,1]))

    print hsv_image.shape
    #hsv = cv2.split(hsv_image)
    #array_pom=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    array_pom=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #array_hsv = np.zeros(shape=(3, 16))
    array_hsv = [0,0,0]


    for i in (0,1,2):
        for x in range(len(hsv_image)):
            for y in range(len(hsv_image[x])):
                value = hsv_image.item(x,y,i) 
                index = value/16
                array_pom[index]=array_pom[index]+1
        print array_pom
        array_hsv[i]=array_pom
        array_pom=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    print array_hsv
    print "konec metody"
    return array_hsv

def kl(p, q):
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def L1(v1, v2):
    if(len(v1)!=len(v2)):
        print "error"
        return -1
    return sum([abs(v1[i]-v2[i]) for i in range(len(v1))])

#prepare_annotations()
count_train_histogram()
count_test_histogram()