"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import pickle

import config

class Pictures:
    name = ""
    keywords = []
    rgb = [0,0,0]
    lab = [0,0,0]
    hsv = [0,0,0]
    
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
    

def exportDataToFile(listPictures):
    # ulozim seznam do souboru do dump.py
    pickle.dump(listPictures, open(config.DATAFILE, "w"))
    print config.DATAFILE

def importDateFromFile():
    data = pickle.load(open(config.DATAFILE, "r"))
    return data