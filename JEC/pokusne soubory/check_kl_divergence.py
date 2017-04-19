import numpy as np
import math
import cv2
import pickle
import class_pictures

class Pictures:
    name = ""
    keywords = []
    our_assignment_keywords=[]
    rgb = None
    lab = None
    hsv = None #np.zeros(shape=(3, 16), dtype=float32)
    neighbors = None
    nereast_neighbors = None

def importDataFromFile(fileName):
    data = pickle.load(open(fileName, "r"))
    return data

def kl(a, b):
    a = np.asarray(a, dtype=np.float)
    b = np.asarray(b, dtype=np.float)

    sum = 0
    for i in range(len(a)):
        """The KL divergence is defined only if Q(i)=0 implies P(i)=0, for all i (absolute continuity)"""
        #if(a[i] != 0 and b[i] != 0):
        if(a[i] != 0): # tohle by melo byt spravne ale hazi to chybu
            if(b[i] ==0):
                sum = sum + a[i] * math.log(a[i] / (b[i] + 0.0000001), math.e)
            else:
                sum = sum + a[i] * math.log(a[i] / b[i], math.e)
            #sum = sum + a[i] * (math.log(a[i]) -  math.log(b[i]))
        
    return sum

    #return np.sum(np.where(a != 0, a * np.log(a / b), 0)) # stazeny z internetu


test_data = importDataFromFile("datafile_test.py")

#na malym
a = np.asarray([1,1,1,1,1,1,1], dtype=np.float32)
b = np.asarray([1,1,1,1,1,1,2], dtype=np.float32)
print cv2.compareHist(a, b, cv2.HISTCMP_KL_DIV)
print kl([1,1,0,1,1,1,1,1], [1,1,0,1,1,1,1,2])

#zretezeni
histogram1 = np.zeros(shape=(3*16), dtype=np.float32)

i=0
for slozka in test_data[0].lab:
    for pixel in slozka:
        histogram1[i] = pixel
        i = i+1
    print slozka

print histogram1
histogram2 = np.zeros(shape=(3*16), dtype=np.float32)
i=0
for slozka in test_data[1].lab:
    for pixel in slozka:
        histogram2[i] = pixel
        i = i+1
        

print cv2.compareHist(test_data[0].lab, test_data[1].lab, cv2.HISTCMP_KL_DIV)
print "------------"
print cv2.compareHist(histogram1, histogram2, cv2.HISTCMP_KL_DIV)
print kl(histogram1, histogram2)
