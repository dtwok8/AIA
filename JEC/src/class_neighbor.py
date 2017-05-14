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
    gabor_distance = 0
    gabor_distance_scale = 0
    poem_distance = 0
    poem_distance_scale = 0
    jec = 0
    
    
    def __init__(self, picture):
        self.picture = picture
        