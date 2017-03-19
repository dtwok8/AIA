# -*- coding: utf-8 -*-
"""
Spocita vzdalenosti mezi testovacima histogramama a testovacima histograma. Naskaluje vysledky na 0-1. Slozi dohromady jednotlive vysledky (JEC)
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
""" 

import cv2
import numpy as np
from Queue import PriorityQueue

#moje
import class_pictures
import class_neighbor
import config


class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item


def add_items_to_queue(test_image):
    print "metoda"
    queue = MyPriorityQueue()
    
    for item in test_image.neighbors:
        queue.put(item, item.jec)
        print "pridano"
    return queue
    

def label_transfer(test_image):
    print "ahoj"
    




#queue = MyPriorityQueue()
#queue.put('item1.3', 0.3)
#queue.put('item1', 1)
#queue.put('item3', 3)
#queue.put('item6', 6)
#queue.put('item2', 2)
#
#print queue.get()
#print queue.get()
#print queue.get()
#print queue.get()
#print queue.get()
#train_data = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)

train_data = class_pictures.importDateFromFile(config.DATAFILE_TRAIN)
test_data = class_pictures.importDateFromFile(config.DATEFILE_TEST_NEIGHBORS)

print test_data[0].name
print test_data[0].keywords
print test_data[0].neighbors


for item in test_data:
    print item.neighbors[0]
    fronta = add_items_to_queue(item)
    
while not fronta.empty():   
    print fronta.get()
exit()

#
#label_transfer(train_data, test_data[0])
