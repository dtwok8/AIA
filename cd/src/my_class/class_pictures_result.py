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
#    rgb = None
#    lab = None
#    hsv = None #np.zeros(shape=(3, 16), dtype=float32)
#    neighbors = None
#    nereast_neighbors = None


    def __init__(self, name, keywords_by_human_in_string, keywords_by_automat_in_string):
        self.data = []
        self.name = name
        
        keywords_by_human_in_string = keywords_by_human_in_string.strip() # odstrani /n nakonci
        self.keywords = keywords_by_human_in_string.split(" ")
        
        keywords_by_automat_in_string = keywords_by_automat_in_string.strip() # odstrani /n nakonci
        self.our_assignment_keywords = keywords_by_automat_in_string.split(" ")
     
        
def importDataFromFile(fileName):
    """
        Importuje data ze souboru.
        
        Keyword arguments:
            fileName -- nazev souboru ze ktereho maji byt data ziskana.
        
        Return:  
            data -- data ziskana ze souboru..
    """
    try:
        data = pickle.load(open(fileName, "r"))
    except: 
        print("Pri nacitani dat ze souboru {} nastala chyba. Zkontrolujte jmeno souboru a zda existuje.").format(fileName)
        sys.exit(1)
    
    return data