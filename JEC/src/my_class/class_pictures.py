"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import pickle
import numpy as np
import sys

import config


class Pictures:
    name = ""
    keywords = []
    our_assignment_keywords=[]
    rgb = None
    lab = None
    hsv = None #np.zeros(shape=(3, 16), dtype=float32)
    gabor = None
    gaborq = None
    poem = None
    color_poem = None
    haar = None
    haarq = None
    neighbors = None
    nereast_neighbors = None
    
    
    def __init__(self, name, keywords_by_human_in_string, keywords_by_automat_in_string = None):
        self.data = []
        self.name = name
        
        keywords_by_human_in_string = keywords_by_human_in_string.strip() # odstrani /n nakonci
        self.keywords = keywords_by_human_in_string.split(" ")
        
        if(keywords_by_automat_in_string is not None):
            keywords_by_automat_in_string = keywords_by_automat_in_string.strip() # odstrani /n nakonci
            self.our_assignment_keywords = keywords_by_automat_in_string.split(" ")
            
    
    #nejde mi to rozchodit
    def setKeywords(self, keywordsInString): 
        keywordsInString = keywordsInString.strip() # odstrani /n nakonci
        self.keywords = keywordsInString.split(" ")
        print self.keywords
    

#asi budu posilat jmeno souboru jako parametr
def exportDataToFile(listPictures, fileName):
    try:
        # ulozim seznam do souboru, ktery je uveden jako datafile v configu
        pickle.dump(listPictures, open(fileName, "w"))
    except:
        print("Pri exportu do souboru doslo k chybe.")
        sys.exit(1)
        
        

def importDataFromFile(fileName):
    
    try:
        data = pickle.load(open(fileName, "r"))
    except: 
        print("Pri nacitani dat ze souboru {} nastala chyba. Zkontrolujte jmeno souboru a zda existuje.").format(fileName)
        sys.exit(1)
    return data