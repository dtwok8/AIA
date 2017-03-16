"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import pickle
import config
import numpy as np

class Neighbor:
    picture = None
    combining_distance = 0
    rgb_distance = 0
    rgb_distance_scale = 0 
    lab_distance = 0
    lab_distance_scale = 0 
    hsv_distance = 0
    hsv_distance_scale = 0 
    
    def __init__(self, picture):
        self.picture = picture
        

#asi budu posilat jmeno souboru jako parametr
def exportDataToFile(listPictures, fileName):
    # ulozim seznam do souboru, ktery je uveden jako datafile v configu
    pickle.dump(listPictures, open(fileName, "w"))

def importDateFromFile(fileName):
    data = pickle.load(open(fileName, "r"))
    return data