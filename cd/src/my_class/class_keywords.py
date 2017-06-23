"""
Objekt Keywords.

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
    