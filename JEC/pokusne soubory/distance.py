"""
Objekt Pictures a k nemu prislusne a potrebne metody jako zapsani objektu do souboru nebo naopak export objektu ze souboru.

@author: Katerina Kratochvilova
"""

import math

def kl(histogram1, histogram2):
    a = np.zeros(shape=(3*16), dtype=np.float32)
    i=0
    for slozka in histogram1:
        for pixel in slozka:
            a[i] = pixel
            i = i+1

    b = np.zeros(shape=(3*16), dtype=np.float32)
    i=0
    for slozka in histogram2:
        for pixel in slozka:
            b[i] = pixel
            i = i+1
    
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