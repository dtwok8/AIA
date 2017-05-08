# -*- coding: utf-8 -*-
"""
Nacita testovaci mnozinu obrazku, a ziskává histogramy. 
Created on Wed Sep 21 15:02:46 2016

@author: Katerina Kratochvilova
"""

import cv2
import numpy as np
import math


from matplotlib import pyplot as plt
 
DEBUG = True 
COUNT_DIRECTIONS = 3
CELL_SIZE = 3 #7
BLOCK_SIZE = 8 #10
TAU = 4
 
def write_matrix_file(matrix, file_name):
    soubor = open(file_name, 'w')
    for row in matrix:
        for item in row:
            soubor.write(" {} ".format(item))
        soubor.write("\n")
    soubor.close()    

    
def count_gradient(img):
    ddepth = -1; #when ddepth=-1, the output image will have the same depth as the source.

    img = img.astype(float) #prevedeme obrazek na float, v zakladu je uint, kdyz to neudelame tak nam misto zapornych cisel vyjde v gradientech 0
    
    x_kernel = np.array([1.0, 0.0, -1.0]).reshape((1,3))
    y_kernel = np.array([1.0, 0.0, -1.0])
    #x_kernel = np.array([-1.0, 1.0]).reshape((1,2))
    #y_kernel = np.array([-1.0, 1.0])
    
    gradient = np.zeros((2, img.shape[0], img.shape[1]), dtype = float)
    gradient[0,:,:] = cv2.filter2D(img, ddepth, x_kernel, borderType=cv2.BORDER_REPLICATE)
    gradient[1,:,:] = cv2.filter2D(img, ddepth, y_kernel, borderType=cv2.BORDER_REPLICATE)
        
    return gradient

    
def count_magnitude(gradient):
    magnitude = np.zeros(gradient[0].shape, dtype=np.float)

    for row in range(len(gradient[0])):
        for column in range (len(gradient[0,row])):
            magnitude[row, column] = math.sqrt(gradient[0, row, column] * gradient[0, row, column] + gradient[1, row, column] * gradient[1, row, column] + gradient[2, row, column] * gradient[2, row, column])

    if(DEBUG):
        cv2.imwrite('magnitude.jpg', magnitude)
        
    return magnitude

def count_phase(gradient):
    phase = cv2.phase(gradient[1,:,:], gradient[2,:,:], angleInDegrees=False)
#    phase = np.zeros(gradient[0].shape, dtype = float)
#    for row in range(len(gradient[0])):
#        for column in range(len(gradient[0,0])):
#            v1 = (gradient[0][row][column], gradient[1][row][column], gradient[2][row][column])
#            v2 = (gradient[0][row][column], gradient[1][row][column], 0.0)
#            phase[row, column] = angle_between(v1, v2) 
#            if math.isnan(phase[row, column]):
#                print "{} - {}".format(v1, v2)
    #angleInDegrees – when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    
    if (DEBUG):
        write_matrix_file(phase, "phase_3.txt")
        
    return phase


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    
    if(v1 == (0,0,0) or v2 == (0,0,0)):
        return 0
    
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def compute_direction(count_directions, gradient, magnitude, phases): 
    """
        Spocita uhly kam vektor smeruje a rozradi se do matic podle smeru (pocet smeru = count_directions)
    """
    
    if (DEBUG):
        write_matrix_file(phases, "phase.txt")
    
    size_of_direction = 2 * math.pi / count_directions
    
    #vytvoreni matice na magnitudy rozrazene podle smeru
    directional = np.zeros((count_directions, gradient[0].shape[0], gradient[0].shape[1]), dtype=float)
    
    for x in range(len(phases)):
        for y in range(len(phases[x])):            
            for i in range(count_directions):
                if(phases[x][y] >= (i*size_of_direction) and phases[x][y] < ((i+1)*size_of_direction)):
                    directional[i][x][y] = magnitude[x][y]

    if (DEBUG):
    
        for i in range(len(directional)):
            write_matrix_file(directional[i,:,:], "directional_3_{}.txt".format(i))
            cv2.imwrite('directional_3_{}.jpg'.format(i), directional[i,:,:])

    return directional


def compute_aems(count_directions, cell_size, directional):
    """
    
    """
    # use either convolution or integral image
    kernel = np.ones((cell_size, cell_size)) 
    kernel = kernel[:,:]/(cell_size*cell_size)  
    aems = np.zeros((count_directions, img.shape[0], img.shape[1]), dtype=float)
    for d in range(count_directions):
        aems[d, :, :] = cv2.filter2D(directional[d, :, :], -1, kernel, borderType=cv2.BORDER_REPLICATE)
    
    
    if (DEBUG):
        for d in range(len(aems)):
            write_matrix_file(aems[d,:,:], "aems_3_{}.txt".format(d))
            cv2.imwrite('aems_3_{}.jpg'.format(d), aems[d,:,:])

    return aems
    
        
def compute_lbp(directions, aems, block_size, tau):
    bordersize = block_size / 2 + 1
    
    lbp = np.zeros(aems.shape, dtype=np.uint8)
    for d in range(directions):
        border_img = cv2.copyMakeBorder(aems[d, :, :], top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_REPLICATE)

        for r in range(bordersize, border_img.shape[0] - bordersize):
            #print r
            for c in range(bordersize, border_img.shape[1] - bordersize):
                #print r, c 
                #do LBP posilam cely block
                lbp[d, r - bordersize, c - bordersize] = compute_lbp_value(r, c, border_img, block_size, tau)
                #break
            #break
        #break
        
        if (DEBUG):
            for i in range(len(lbp)):
                write_matrix_file(lbp[i,:,:], "lbp_3_{}.txt".format(i))
                cv2.imwrite('lbp_3_{}.png'.format(i), lbp[i,:,:])
    return lbp


def compute_lbp_value(r, c, border_img, block_size, tau):
    radius = float(block_size) / 2

    val = 0
    center = border_img[r, c]
    #print "Computing lbp val for", repr(r), repr(c), "center val:", center
    count_pixels = 8
    for i in range(count_pixels): # vyberu si jen 8 pixelu z celeho kola
    #2 * np.pi / cout_pixels - rozdelim celou periodu pi na 8 casti a vezmu vzdycky i-tou cast, tu stcim do konsinu a posunu to na okraj radius
        x = c -1 + np.cos(i * 2 * np.pi / count_pixels) * radius # zjistit pozici pixelu
        y = r -1 + np.sin(i * 2 * np.pi / count_pixels) * radius #zjistit pozici pixelu
        #print "border_img[{}, {}] center[{},{}]> {}".format(x,y, r,c,center)
        v = border_img[int(y), int(x)] # hodnota pixelu 
        #if (v - center) >= tau: 
        if (v > center):
            val += np.power(2, i) # 2 na i-tou

    return val


def count_gradient_3(img):   
    #print img.shape #(360, 480, 3)
    # pro kazdou barvu zjistim gradienty pro x a y
    gradient_b = count_gradient(img[:,:,0])
    gradient_g = count_gradient(img[:,:,1])
    gradient_r = count_gradient(img[:,:,2])
    
    #ziskam dve trojrozmerne vektory
    vektor_x = np.array([gradient_b[0], gradient_g[0], gradient_r[0]])
    vektor_y = np.array([gradient_b[1], gradient_g[1], gradient_r[1]])
    
    # z tohohle mi musi vypadnout jeden vektor o velikosti x, y, z - soucet vektoru
    vektor = np.array([vektor_x[0, :, :] + vektor_y[0, :, :], vektor_x[1, :, :] + vektor_y[1, :, :], vektor_x[2, :, :] + vektor_y[2, :, :]]) 
    
    if (DEBUG):
        cv2.imwrite('gradient_b_x.jpg', gradient_b[0,:])
        cv2.imwrite('gradient_b_y.jpg', gradient_b[1,:])
        
        cv2.imwrite('gradient_g_y.jpg', gradient_g[0,:])
        cv2.imwrite('gradient_g_y.jpg', gradient_g[1,:])
        
        cv2.imwrite('gradient_r_x.jpg', gradient_r[0,:])
        cv2.imwrite('gradient_r_y.jpg', gradient_r[1,:])
        
        cv2.imwrite('gradient_3_x.jpg', vektor[0,:,:])
        cv2.imwrite('gradient_3_y.jpg', vektor[1,:,:])
        cv2.imwrite('gradient_3_z.jpg', vektor[2,:,:])
    
        write_matrix_file(vektor[0,:,:], 'gradient_3_x.txt')
        write_matrix_file(vektor[1,:,:], 'gradient_3_y.txt')
        write_matrix_file(vektor[2,:,:], 'gradient_3_z.txt')
    return vektor

img = cv2.imread("../../../Data/iaprtc12/images/00/51.jpg")

#spoctu gradient
gradient = count_gradient_3(img)
magnitude = count_magnitude(gradient)
phase = count_phase(gradient)

directional = compute_direction(COUNT_DIRECTIONS, gradient, magnitude, phase)
aems = compute_aems(COUNT_DIRECTIONS, CELL_SIZE, directional)

lbp = compute_lbp(COUNT_DIRECTIONS, aems, BLOCK_SIZE, TAU)


print angle_between((1, 0, 0), (0, 1, 0))
print angle_between((5, 3, 8), (5, 3, 0))
print angle_between((0, -5, 5), (0, 5, 0))
#10

exit()

