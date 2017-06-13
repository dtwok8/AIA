"""
Objekt Keywords a k nemu prislusne a potrebne metody.

@author: Katerina Kratochvilova
"""

import pickle
import numpy as np

import config


class Keywords:
    keyword = ""
    w_auto=0
    w_human=0
    w_correctly = 0
    precision = 0
    recall = 0
    
    
    def __init__(self, keyword):
        self.keyword = keyword
    

#asi budu posilat jmeno souboru jako parametr
#def exportDataToFile(listKeywords, fileName):
    # ulozim seznam do souboru, ktery je uveden jako datafile v configu
#    pickle.dump(listPictures, open(fileName, "w"))

#def importDataFromFile(fileName):
#    data = pickle.load(open(fileName, "r"))
#    return data