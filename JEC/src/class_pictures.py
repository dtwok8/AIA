"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import pickle
import numpy as np

import config


class Pictures:
    name = ""
    keywords = []
    our_assignment_keywords=[]
    rgb = None
    lab = None
    hsv = None #np.zeros(shape=(3, 16), dtype=float32)
    neighbors = None
    nereast_neighbors = None
    
    
    def __init__(self, name, keywordsInString=[]):
        self.data = []
        self.name = name
        
        keywordsInString = keywordsInString.strip() # odstrani /n nakonci
        self.keywords = keywordsInString.split(" ")
    
#    def __init__(self, name, keywordsByHumanInString, keywordsByAutomatInString):
#        self.data = []
#        self.name = name
#        
#        keywordsByHumanInString = keywordsByHumanInString.strip() # odstrani /n nakonci
#        self.keywords = keywordsByHumanInString.split(" ")
#        
#        keywordsByAutomatInString = keywordsByAutomatInString.strip() # odstrani /n nakonci
#        self.our_assignment_keywords = keywordsByAutomatInString.split(" ")
    
    #nejde mi to rozchodit
    def setKeywords(self, keywordsInString): 
        keywordsInString = keywordsInString.strip() # odstrani /n nakonci
        self.keywords = keywordsInString.split(" ")
        print self.keywords
    

#asi budu posilat jmeno souboru jako parametr
def exportDataToFile(listPictures, fileName):
    # ulozim seznam do souboru, ktery je uveden jako datafile v configu
    pickle.dump(listPictures, open(fileName, "w"))

def importDataFromFile(fileName):
    data = pickle.load(open(fileName, "r"))
    return data