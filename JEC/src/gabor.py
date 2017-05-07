import numpy as np
import math
import cv2

#moje
import class_pictures
import config
 
def build_filters(psi):
    filters = []
    ksize = 7
    sigma = 0.5 
    gamma = 1
    for theta in (0, math.pi/4, math.pi/2, (3/4)*math.pi):
        for lambdaa in (2, 2*math.sqrt(2), 4): 
            kern = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambdaa, gamma, psi)
            #kern /= 1.5*kern.sum() #normovani #proc? bez toho je jen cerno kdyz mam nasteveny lambdu na 2
            filters.append(kern)
    return filters


def use_filters(img, filters):
    filtered_img = []
    ddepth = -1 #when ddepth=-1, the output image will have the same depth as the source.
    
    i=1
    for kern in filters:
        fimg = cv2.filter2D(img, ddepth, kern)
        filtered_img.append(fimg)

        #cv2.imwrite("gabor_filter_img{}.jpg".format(i), fimg)

        i = i+1
    
    return filtered_img
    
    
def count_phase(filtered_img_real, filtered_img_imag):
    phase = []

    for i in range(len(filtered_img_real)):
        cv2.phase(filtered_img_real[i], filtered_img_imag[i], angleInDegrees=False)
        #angleInDegrees - when true, the input angles are measured in degrees, otherwise, they are measured in radians.
    return phase


def count_magnitude(filtered_img_real, filtered_img_imag):
    magnitude = []
    
    for i in range(len(filtered_img_real)):
        magnitude.append(cv2.magnitude(filtered_img_real[i], filtered_img_imag[i]))
    
    return magnitude
    
 
def count_vector(magnitudes, deep): 
    """
    Nasklada vektory za sebe
    """

    array_histograms_magnitude = np.zeros(shape=(deep*len(magnitudes)), dtype=np.int)

    for i in range(len(magnitudes)): 
        for x in range(len(magnitudes[i])):
            for y in range(len(magnitudes[i][x])):
                value = magnitudes[i].item(x,y) 
                index = ((i*deep))+int((value/deep)) # (i*deep) potrebuju se posunout na i-ty filtrovany obrazek
                array_histograms_magnitude[index]=array_histograms_magnitude[index]+1
    return array_histograms_magnitude
 
def count_magnitude(filtered_img_real, filtered_img_imag):
    magnitudes = np.zeros(shape=(len(filtered_img_real), len(filtered_img_real[0]),len(filtered_img_real[0][0])), dtype=np.int)
    
    for i in range(len(filtered_img_real)):
        magnitudes[i] = cv2.magnitude(filtered_img_imag[i], filtered_img_real[i])

    m_min = 0
    m_max = 360
    
    for i in range(len(magnitudes)):
        for x in range(len(magnitudes[i])):
            for y in range(len(magnitudes[i][x])):
                if (magnitudes[i].item(x,y) > 360):
                    print "chyba!!"
                    
                magnitudes[i][x,y] =  254* (magnitudes[i].item(x,y) /m_max)
    
    return magnitudes

#def count_gabor(img):
#    "Gabor pocitame pouze s realnou casti."
#    
#    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    img = img.astype(float)
#    vector_deep = 16
#    
#    #gabor
#    filters_real = build_filters(0)
#    filtered_img_real = use_filters(img, filters_real)
#    
#    gabor_vector = count_vector(filtered_img_real, vector_deep) 
#    return gabor_vector


def count_gabor(img):
    "Gabor pocitame pouze s realnou casti."
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(float)
    vector_deep = 16
    
    #gabor
    filters_real = build_filters(0)
    filtered_img_real = use_filters(img, filters_real)
    
    filters_imag = build_filters((math.pi/2)) 
    filtered_img_imag = use_filters(img, filters_imag)
    
    magnitude = count_magnitude(filtered_img_real, filtered_img_imag)
    gabor_vector = count_vector(magnitude, vector_deep)
    #gabor_vector = count_vector(filtered_img_real, vector_deep) 
    
    return gabor_vector


def count_gabor_q(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.astype(float)
    
    filters_real = build_filters(0)
    filters_imag = build_filters((math.pi/2))
    filtered_img_real = use_filters(img, filters_real) 
    filtered_img_imag = use_filters(img, filters_imag)    
    
    phase = count_phase(filtered_img_real, filtered_img_imag)
    return phase
    