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
    
    if (DEBUG):
        write_matrix_file(gradient[0], "gradientX.txt")
        write_matrix_file(gradient[1], "gradientY.txt")
        cv2.imwrite('gradientX.png', gradient[0,:,:])
        cv2.imwrite('gradientY.png', gradient[1,:,:])
    
    return gradient

    
def count_magnitude(gradient):
    magnitude = cv2.magnitude(gradient[0,:,:],gradient[1,:,:])
    
    if (DEBUG):
        write_matrix_file(magnitude, "magnitude.txt")
        cv2.imwrite('magnitude.png', magnitude)
        
    return magnitude

def count_phase(gradient):
    phase = cv2.phase(gradient[0,:,:], gradient[1,:,:], angleInDegrees=False)
    #angleInDegrees – when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    
    if (DEBUG):
        write_matrix_file(phase, "phase.txt")
        
    return phase

def compute_direction(count_directions, gradient, magnitude): 
    """
        Spocita uhly kam vektor smeruje a rozradi se do matic podle smeru (pocet smeru = count_directions)
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
                if(phases[x][y] >= (i*size_of_direction) and phases[x][y] < ((i+1)*size_of_direction)):
                    directional[i][x][y] = magnitude[x][y]

    if (DEBUG):
    
        for i in range(len(directional)):
            write_matrix_file(directional[i,:,:], "directional{}.txt".format(i))
            cv2.imwrite('directional{}.png'.format(i), directional[i,:,:])

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
            write_matrix_file(aems[d,:,:], "aems{}.txt".format(d))
            cv2.imwrite('aems{}.png'.format(d), aems[d,:,:])

    return aems
    
        
def compute_lbp(directions, aems, block_size, tau):
    bordersize = block_size / 2 + 1
    
    lbp = np.zeros(aems.shape, dtype=np.uint8)
    for d in range(len(directions)):
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
                write_matrix_file(lbp[i,:,:], "lbp{}.txt".format(i))
                cv2.imwrite('lbp{}.png'.format(i), lbp[i,:,:])
    return lbp


def compute_lbp_value(r, c, border_img, block_size, tau):
    radius = float(block_size) / 2

    val = 0
    center = border_img[r, c]
    #print "Computing lbp val for", repr(r), repr(c), "center val:", center
    count_pixels = 8
    for i in range(count_pixels): # vyberu si jen 8 pixelu z celeho kola
    #2 * np.pi / cout_pixels - rozdelim celou periodu pi na 8 casti a vezmu vzdycky i-tou case, tu stcim do konsinu a posunu to na okraj radius
        x = np.cos(i * 2 * np.pi / count_pixels) * radius
        y = np.sin(i * 2 * np.pi / count_pixels) * radius
        #print x, y
        if False: # self.interpolation:      
            v = 0#interpolate(c + x, r - y, border_img)
        else:
            v = border_img[int(y), int(x)]
            #print "value", v
        #if (v - center) >= self.tau:
        #  val += 1
        #val = val << 1;   
        if (v - center) >= tau:       
            val += np.power(2, i) # 2 na i-tou
        #print "akt lbp val:", val
    return val



img = cv2.imread("../../Data/iaprtc12/images/00/51.jpg")

#print img.shape #(360, 480, 3)

# pro kazdou barvu zjistim gradient x a gradient y
gradient_b = count_gradient(img[:,:,0])
gradient_g = count_gradient(img[:,:,1])
gradient_r = count_gradient(img[:,:,2])

vektor_x = np.array([gradient_b[0], gradient_g[0], gradient_r[0]])
vektor_y = np.array([gradient_b[1], gradient_g[1], gradient_r[1]])
# z tohohle mi musi vypadnout jeden vektor o velikosti x, y, z
#soucet vektoru
vektor = np.array([vektor_x[0, :, :] + vektor_y[0, :, :], vektor_x[1, :, :] + vektor_y[1, :, :], vektor_x[2, :, :] + vektor_y[2, :, :]]) 
print gradient_b[0,0,0]
print gradient_b[1,0,0]
print vektor[0,0,0]

print vektor.shape
cv2.imwrite('gradient_3_x.png', vektor[0,:,:])
cv2.imwrite('gradient_3_y.png', vektor[1,:,:])
cv2.imwrite('gradient_3_z.png', vektor[2,:,:])

magnituda = np.zeros(vektor[0].shape, dtype=np.float)

for row in range(len(vektor[0])):
    for column in range (len(vektor[0,row])):
        magnituda[row, column] = math.sqrt(vektor[0, row, column] * vektor[0, row, column] + vektor[1, row, column] * vektor[1, row, column] + vektor[2, row, column] * vektor[2, row, column])


print magnituda.shape
cv2.imwrite('magnituda_3_z.png', magnituda)

exit()

#img = np.float32(img) / 255.0

count_directions = 3
cell_size = 7
block_size = 10
tau = 4
gradient = count_gradient(img)
magnitude = count_magnitude(gradient) 
directional = compute_direction(count_directions, gradient, magnitude)
aems = compute_aems(count_directions, cell_size, directional)

compute_lbp(directional, aems, block_size, tau)

exit()
aems = compute_aems(directional, img)
lbp = compute_lbp(directions, aems)

print lbp.shape
print lbp

cv2.imwrite('lbp.png', lbp[0,:,:])


        
soubor.close()

soubor = open("img.txt", 'w')  
for row in img:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()



# Python gradient calculation 
print "---------------------------------" 
# Read image
img = cv2.imread('../../Data/iaprtc12/images/01/1210.jpg', 0)
#img = np.float32(img) / 255.0
 
# Calculate gradient 
#gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
#gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)

# Python Calculate gradient magnitude and direction ( in degrees ) 
mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)

print angle.shape
print mag.shape

soubor = open("angle.txt", 'w')  
for row in angle:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()

soubor = open("mag.txt", 'w')  
for row in mag:
    for item in row:
        soubor.write(" {} ".format(item))
    soubor.write("\n")
soubor.close()
exit()
#smery = compute_direction(directions, gradient, mag)
#print smery.shape

directional = np.zeros((3, 360, 480), dtype=float)
print angle.shape
print directional.shape
for i in range(len(angle)):
    for y in range(len(angle[i])):
        if(angle[i][y] >= 0 and angle[i][y] < 120):
            directional[0][i][y] = magnitude[i][y]
        if(angle[i][y] >= 120 and angle[i][y] < 270):
            directional[1][i][y] = magnitude[i][y]
        if(angle[i][y] >= 270 and angle[i][y] < 360):
            directional[2][i][y] = magnitude[i][y] 
                
cv2.imwrite('directional1.png', directional[0,:,:])
cv2.imwrite('directional2.png', directional[1,:,:])
cv2.imwrite('directional3.png', directional[2,:,:])
                
exit()

#Compute gradient magnitude at each pixel

bin_size = 2 * np.pi / directions
directional = np.zeros((directions, img.shape[0], img.shape[1]), dtype=float)

x = np.array([-1, +1, +1, -1])
y = np.array([-1, -1, +1, +1])
asd = np.arctan2(y, x) * 180 / np.pi
print asd


print dirs

# do jakeho kvadrantu to patri bezva porad mi vychazi jen ten prvni
print dirs.shape
#print "{} {} {}".format(gradient[0,350,479], gradient[1,350,479], dirs[350,479])

 




exit()
dirs[dirs < 0] = 0
mags = np.sqrt(gradient[0,:,:]**2 + gradient[1,:,:]**2) #znova pocitam magnitudu ?

for d in range(directions):
      lower = d * bin_size
      upper = (d + 1) * bin_size
      directional[d] = dirs
      directional[d][directional[d] < lower] = 0
      directional[d][directional[d] > upper] = 0
      directional[d][directional[d] > 0] = 1 
      directional[d] *= mags

print directional

    
    
cv2.imwrite('directional1.png', directional[0,:,:])
cv2.imwrite('directional2.png', directional[1,:,:])
cv2.imwrite('directional3.png', directional[2,:,:])

