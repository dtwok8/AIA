"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import pickle
import config
import numpy as np

class Distances:
    test_img_name = ""
    keywords = []
    rgb = None
    lab = None
    hsv = None #np.zeros(shape=(3, 16), dtype=float32)
   
    
    def __init__(self, name, keywordsInString):
        self.data = []
        self.name = name
        
        keywordsInString = keywordsInString.strip() # odstrani /n nakonci
        self.keywords = keywordsInString.split(" ")
    
    #nejde mi to rozchodit
    def setKeywords(self, keywordsInString): 
        keywordsInString = keywordsInString.strip() # odstrani /n nakonci
        self.keywords = keywordsInString.split(" ")
        print self.keywords
    

#asi budu posilat jmeno souboru jako parametr
def exportDataToFile(listPictures, fileName):
    # ulozim seznam do souboru, ktery je uveden jako datafile v configu
    pickle.dump(listPictures, open(fileName, "w"))

def importDateFromFile(fileName):
    data = pickle.load(open(fileName, "r"))
    return data