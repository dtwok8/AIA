# -*- coding: utf-8 -*-
"""
Poem slouzi k detekci hran.

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np
import math
import sys #srgv

from matplotlib import pyplot as plt
 
DEBUG = True 
COUNT_DIRECTIONS = 3
CELL_SIZE = 3 #7
BLOCK_SIZE = 8 #10
TAU = 4
 
def write_matrix_file(matrix, file_name):
    """
    Zapise zaslanou matici do souboru.
    
    Keyword arguments:
            matrix -- matice, ktera ma byt ulozena do souboru. 
            file_name -- nazev souboru do ktereho se ma matice ulozit.
    """
    soubor = open(file_name, 'w')
    for row in matrix:
        for item in row:
            soubor.write(" {} ".format(item))
        soubor.write("\n")
    soubor.close()    

    
def count_gradient(img):
    """
    Spocita gradienty obrazku (smery rustu), tak ze na nej pouzije masky x_kernel a y_kernel.
    
    Keyword arguments:
            img -- obrazek, pro ktery se ma gradient spocitat. 
    Return arguments:
            gradient -- vypocteny gradient.
    """
    ddepth = -1; #when ddepth=-1, the output image will have the same depth as the source.

    img = img.astype(float) #prevedeme obrazek na float, v zakladu je uint, kdyz to neudelame tak nam misto zapornych cisel vyjde v gradientech 0
    
    x_kernel = np.array([1.0, 0.0, -1.0]).reshape((1,3))
    y_kernel = np.array([1.0, 0.0, -1.0])
    #x_kernel = np.array([-1.0, 1.0]).reshape((1,2))
    #y_kernel = np.array([-1.0, 1.0])
    
    gradient = np.zeros((2, img.shape[0], img.shape[1]), dtype = float)
    gradient[0,:,:] = cv2.filter2D(img, ddepth, x_kernel, borderType=cv2.BORDER_REPLICATE)
    gradient[1,:,:] = cv2.filter2D(img, ddepth, y_kernel, borderType=cv2.BORDER_REPLICATE)
    
    if (DEBUG):
        write_matrix_file(gradient[0], "gradientX.txt")
        write_matrix_file(gradient[1], "gradientY.txt")
        cv2.imwrite('gradientX.jpg', gradient[0,:,:])
        cv2.imwrite('gradientY.jpg', gradient[1,:,:])
    
    return gradient

    
def count_magnitude(gradient):
    """"
    Spocte magnitudu, velikost smeru rustu. Magnituda = velikost vektoru.
    
    Keyword arguments:
            gradient -- gradient pro ktery se ma magnituda spocitat. 
    Return arguments:
            magnitude -- vypoctene magnitudy.
    """
    magnitude = cv2.magnitude(gradient[0,:,:],gradient[1,:,:])
    
    if (DEBUG):
        write_matrix_file(magnitude, "magnitude.txt")
        cv2.imwrite('magnitude.jpg', magnitude)
        
    return magnitude


def count_phase(gradient):
    """
    Spocita faze (uhly) vektrou gradientu.
    
    Keyword arguments:
        gradient -- gradienty pro ktery se maji uhly spocitat. 
    Return arguments:
        phase -- vypoctene phase.
    """
    phase = cv2.phase(gradient[0,:,:], gradient[1,:,:], angleInDegrees=False)
    
    #angleInDegrees – when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    
    if (DEBUG):
        write_matrix_file(phase, "phase.txt")
        
    return phase


def compute_direction(count_directions, gradient, magnitude): 
    """
        Spocita uhly kam vektor smeruje a rozradi se do matic podle smeru (pocet smeru = count_directions)
        
        Keyword arguments:
            count_directions -- pocet smeru.
            gradient -- gradient.
            magnitude -- magnitudy.
        Return arguments:
            directional -- 3 matice, roztridene podle fazi, obsahujici magnitudy.    
    """
    
    phases = cv2.phase(gradient[0], gradient[1], angleInDegrees=False)
    #angleInDegrees – when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    
    if (DEBUG):
        write_matrix_file(phases, "phase.txt")
    
    size_of_direction = 2 * math.pi / count_directions
    
    #vytvoreni matice na magnitudy rozrazene podle smeru
    directional = np.zeros((count_directions, gradient[0].shape[0], gradient[0].shape[1]), dtype=float)
    
    for x in range(len(phases)):
        for y in range(len(phases[x])):            
            for i in range(count_directions):
                #zarazeni do prislusneho smeru
                if(phases[x][y] >= (i*size_of_direction) and phases[x][y] < ((i+1)*size_of_direction)):
                    directional[i][x][y] = magnitude[x][y]

    if (DEBUG):    
        for i in range(len(directional)):
            write_matrix_file(directional[i,:,:], "directional{}.txt".format(i+1))
            cv2.imwrite('directional{}.jpg'.format(i+1), directional[i,:,:])

    return directional


def compute_aems(count_directions, cell_size, directional):
    """
        Vypocita lokalni histogramu gradientu z okoli.
    
        Keyword arguments:
            count_directions -- pocet smeru. 
            cell_size - velikost cell (okoli).
            directional -- rozsmerovane magnitudy podle fazi.
        Return arguments:
            aems -- vypoctene lokalni histogramy z okoli.
    """
    # use either convolution or integral image
    kernel = np.ones((cell_size, cell_size)) 
    kernel = kernel[:,:]/(cell_size*cell_size)  
    aems = np.zeros((count_directions, directional[0].shape[0], directional[0].shape[1]), dtype=float)
    for d in range(count_directions):
        aems[d, :, :] = cv2.filter2D(directional[d, :, :], -1, kernel, borderType=cv2.BORDER_REPLICATE)
    
    
    if (DEBUG):
        for d in range(len(aems)):
            write_matrix_file(aems[d,:,:], "aems{}.txt".format(d))
            cv2.imwrite('aems{}.jpg'.format(d), aems[d,:,:])

    return aems
    
        
def compute_lbp(directions, aems, block_size, tau):
    """
        LBP. 
    
        Keyword arguments:
            directions -- pocet smeru. 
            aems - vypoctene lokalni histogramy z okoli.
            block_size -- velikost blocku.
            tau -- konstanta, ktera se pripocitava k centralnimu, vhodne pri konstantnim okoli.
        Return arguments:
            lbp -- vypoctene lbp.
    """
    bordersize = block_size / 2 + 1
    
    lbp = np.zeros(aems.shape, dtype=np.uint8)
    for d in range(directions):
        border_img = cv2.copyMakeBorder(aems[d, :, :], top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_REPLICATE)
        write_matrix_file(border_img, "border1{}.txt".format(d))
        
        for r in range(bordersize, border_img.shape[0] - bordersize):
            for c in range(bordersize, border_img.shape[1] - bordersize):
                #do LBP posilam cely block
                lbp[d, r - bordersize, c - bordersize] = compute_lbp_value(r, c, border_img, block_size, tau)
        
        if (DEBUG):
            for i in range(len(lbp)):
                write_matrix_file(lbp[i,:,:], "lbp{}.txt".format(i+1))
                cv2.imwrite('lbp{}.jpg'.format(i+1), lbp[i,:,:])
                write_matrix_file(border_img, "border{}.txt".format(i+1))
                cv2.imwrite('border{}.jpg'.format(i+1), border_img)
                
    return lbp


def compute_lbp_value(r, c, border_img, block_size, tau):
    """
        Vypocte konkretni LBP hodnotu, pro dany pixel. 
    
        Keyword arguments:
            r -- row, radek (zkratka souradnice [r,c]) 
            c -- column, sloupec.
            border_img -- obrazek i s rameckem.
            block_size -- velikost blocku.
            tau -- konstanta, ktera se pripocitava k centralnimu, vhodne pri konstantnim okoli.
        Return arguments:
            val -- vypoctene lbp pro jeden pixel.
    """
    radius = float(block_size) / 2

    val = 0
    center = border_img[r, c]
    #print "Computing lbp val for", repr(r), repr(c), "center val:", center
    count_pixels = 8
    for i in range(count_pixels): # vyberu si jen 8 pixelu z celeho kola
    #2 * np.pi / cout_pixels - rozdelim celou periodu pi na 8 casti a vezmu vzdycky i-tou cast, tu stcim do konsinu a posunu to na okraj radius
        x = c -1 + np.cos(i * 2 * np.pi / count_pixels) * radius # zjistit pozici pixelu
        y = r -1 + np.sin(i * 2 * np.pi / count_pixels) * radius #zjistit pozici pixelu
        v = border_img[int(y), int(x)] # hodnota pixelu 

        if (v >= (center + tau)):
            val += np.power(2, i) # 2 na i-tou

    return val

def compute_histogram(lbp, x = 4, y = 4):
    step_x = len(lbp[0]) /x
    step_y = len(lbp[0,0]) /y 
    print "step_x {} step_y {}".format(step_x, step_y)
    
    for d in range(len(lbp)):
        for row_block in range(x-1):
            for column_block in range(y-1):
                compute_local_histogram(lbp[d], row_block, column_block, step_x, step_y)
    

def compute_local_histogram(lbp, row_block, column_block, step_x, step_y):
    histogram = np.zeros(256)
    
    for x in range(step_x*row_block, step_x*(row_block+1)): #od zacatku blocku, #dokonce blocku po radcich
        for y in range (step_y * column_block, step_y * (column_block+1)): # po sloupcich
            print "{} {} {} lbp: {} ".format(x,y, lbp[x,y])
            index = int(lbp[x,y])
            histogram[index] = histogram[index] + 1
    
    #histogram = histogram / np.sum(histogram) 
    print histogram  


def compute_histogram_experiments(lbp, directions):
    """
        Vypocte globalni histogram na bez rozedelni pravidelnou mrizkou.
        
        Keyword arguments:
            lbp -- lbp.
            directions -- pocet smeru.
        
    """
    
    histogram_size = 256
    histograms = []

    for d in range(len(lbp)):
        histogram = np.zeros(histogram_size)
        for x in lbp[d]:
            for y in x:
                index = y #lbp[d,x,y]
                histogram[index] = histogram[index] + 1
        histogram = histogram / np.sum(histogram) #normalizovani aby soucet hodnot byl 1 pro dany smer
        histograms.append(histogram)
        
        if (DEBUG):
            print histogram
    
    histogram_np = np.zeros(histogram_size * directions)
    for h in range(len(histograms)):
        for i in range(len(histograms[h])):
            histogram_np[(h*256)+i] = histograms[h][i]

    if (DEBUG):
        soubor = open("histogram.txt", 'w')
        
        for item in histogram_np:
            soubor.write("{0:.6f} ".format(item))
            
        soubor.close()


def main():  
    img_name = sys.argv[1]
    img_name = img_name.strip() #odriznuti netisknutelnych znaku
    img = cv2.imread(img_name,0)
    #img = cv2.imread("../../../Data/iaprtc12/images/00/51.jpg", 0)
    
    #factor = 0.5 #zmenseni obrazkuna polovinu
    #img = cv2.resize(img, (0,0), fx=factor, fy=factor) 
    
    gradient = count_gradient(img)
    magnitude = count_magnitude(gradient) 
    directional = compute_direction(COUNT_DIRECTIONS, gradient, magnitude)
    aems = compute_aems(COUNT_DIRECTIONS, CELL_SIZE, directional)

    lbp = compute_lbp(COUNT_DIRECTIONS, aems, BLOCK_SIZE, TAU)

    compute_histogram(lbp)
 
    
main()