"""
Vytvari deskriptor haar.

@author: Katerina Kratochvilova
"""

import numpy as np
import cv2
 
scales = 4

kernel_h = np.array([[1.0, 1.0], [-1.0,-1.0]])
kernel_v = np.array([[-1.0, 1.0], [-1.0,1.0]])
kernel_d = np.array([[1.0, -1.0], [-1.0,1.0]])
kernels = [kernel_h, kernel_v, kernel_d]

def count_histogram(index, histogram, array, deep=16):
    """
        Prevadi histogram 16 binu.
        
        Keyword arguments:
            index -- kolikaty to je obrazek. 
            histogram -- histogram.
            array -- vysledna matice po pouziti filtru.
            deep -- velikost histogramu. 
    """
    
    max = np.amax(array)
    min = np.amin(array)
    
    for row in array:
        for item in row:
            #print item
            #print item, min, max
            i = (((item-min)/(max-min))*16)
            if(i >= 16): # max by to melo byt 16 rovnych, protoze je to max
                i = i-1
                
            histogram[deep*index+i] = histogram[deep*index+i] + 1

    return histogram
    

def count_haar(img):
    """
        Prevede obrazek na sedotonovy. Pouzije filtr vytvorenych z kernelu nahore. 
        Obrazek je nasledne zmensen podle factor. A postup se opakuje. 
        vektor je dlouhy scales x pocet_kernels.
        
        Keyword arguments:
            img -- obrazke pro ktery se haar pocita. 
        Return:
            histogram -- vytvoreny histogram.
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    size = np.amin(img.shape)
    #print size # prepare 4 scales ->  size * f^3 = 64
    factor = np.power((64.0 / size), 1.0/(scales - 1))
    #print "resize_factor:", factor
       
    vector = np.zeros(scales * len(kernels))

    histogram = np.zeros((scales*len(kernels)*16), dtype=np.int)
    
    index = 0
    for scale in range(scales):
        #print "Image shape:", img.shape
        for k in kernels:
            res = cv2.filter2D(img, cv2.CV_16S, k)
            #vector[index] = np.average(res) 
            count_histogram(index,histogram,res) #verze s 16 binovym histogramem
            index += 1
            #cv2.imwrite('haar.jpg', res)
            
            
        img = cv2.resize(img, (0,0), fx=factor, fy=factor) 
    
    return histogram


#img = cv2.imread("img.jpg") 
#count_haar(img)