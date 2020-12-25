"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Iamge Resizing", autori S. Avidan si A. Shamir
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
    
"""


import sys
import cv2 as cv
import numpy as np
import copy
import matplotlib.pyplot as plt

from parameters import *
from select_path import *

import pdb


def compute_energy(img, params):
    """
    calculeaza energia la fiecare pixel pe baza gradientului
    :param img: imaginea initiala
    :return:E - energia
    """
    # urmati urmatorii pasi    
    # 1. transformati imagine in grayscale
    # 2. folositi filtru sobel pentru a calcula gradientul in directia X si Y
    # 3. calculati magnitudinea pentru fiecare pixel al imaginii
    E = np.zeros((img.shape[0],img.shape[1]), np.int16)
    
    img_grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    sobelx = cv.Sobel(img_grayscale, cv.CV_64F, 1, 0, ksize = 3)
    sobely = cv.Sobel(img_grayscale, cv.CV_64F, 0, 1, ksize = 3)
        
    E = (abs(sobelx) + abs(sobely)) / 2
    
    if params.resize_option == 'eliminaObiect':
        cnt = 0
        
        for i in range(0, params.image_obj.shape[0]):
            for j in range(0, params.image_obj.shape[1]):
                if params.image_obj[i][j] == 1:
                    E[i][j]= -32000
                    cnt += 1
                    
        print("Pixeli ramasi din obiect:")
        print(cnt)
    
    return E

def show_path(img, path, color, params):
    new_image = img.copy()
    for row, col in path:
        new_image[row, col] = color

    E = compute_energy(img, params)
    new_image_E = img.copy()
    new_image_E[:,:,0] = E.copy()
    new_image_E[:,:,1] = E.copy()
    new_image_E[:,:,2] = E.copy()

    for row, col in path:
        new_image_E[row, col] = color
    cv.imshow('path img', np.uint8(new_image))
    cv.imshow('path E', np.uint8(new_image_E))
    cv.waitKey(1000)


def delete_path(params : Parameters, img, path):
    """
    elimina drumul vertical din imagine
    :param img: imaginea initiala
    :path - drumul vertical
    return: updated_img - imaginea initiala din care s-a eliminat drumul vertical
            updated_img_obj - masca imaginii initiale cu obiectul de eliminat
    """
    updated_img = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]), np.uint8)
    
    if params.resize_option == "eliminaObiect":
        
        updated_img_obj = np.zeros((params.image_obj.shape[0], params.image_obj.shape[1] - 1), np.uint8)
    
    
    
    for i in range(img.shape[0]):
        col = path[i][1]
        # copiem partea din stanga
        updated_img[i, :col] = img[i, :col].copy()
        
        # copiem partea din dreapta
        updated_img[i, col:] = img[i, col + 1:].copy()
        
        # copiem masca obiectului de eliminat, daca este cazul
        
        if params.resize_option == "eliminaObiect":
            updated_img_obj[i, :col] = params.image_obj[i, :col].copy()
        
            updated_img_obj[i, col:] = params.image_obj[i, col + 1:].copy()
         
    
    if params.resize_option == "eliminaObiect":
        params.image_obj = updated_img_obj
        
    return updated_img

def decrease_width(params: Parameters, num_pixels):
    img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul numarul %i dintr-un total de %d.' % (i+1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol                
        E = compute_energy(img, params)
        path = select_path(E, params.method_select_path)
        
        if params.show_path:
            show_path(img, path, params.color_path, params)
        
        img = delete_path(params, img, path)

    return img

def decrease_height(params: Parameters, num_pixels):
	
    params.image = cv.rotate(params.image, cv.ROTATE_90_CLOCKWISE)
    
    img = decrease_width(params, num_pixels)
    
    img_rotated_back = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    
    params.image = cv.rotate(params.image, cv.ROTATE_90_COUNTERCLOCKWISE)

    return img_rotated_back


def delete_object(params: Parameters, x0, y0, w, h):
    
    original_image = params.image
    
    for i in range(x0, x0 + w):
        for j in range(y0, y0 + h):
            params.image_obj[i, j] = 1
            
    img = decrease_width(params, h)
    
    return img

# Rezolvat masca obiect

def resize_image(params: Parameters):

    
    # redimensioneaza imaginea pe latime
    if params.resize_option == 'micsoreazaLatime':

        resized_image = decrease_width(params, params.num_pixels_width)
        return resized_image
    
    # redimensioneaza imaginea pe inaltime
    elif params.resize_option == 'micsoreazaInaltime':

        resized_image = decrease_height(params, params.num_pixels_height)
        return resized_image
    
    elif params.resize_option == 'amplificaContinut':
        
        originalImage = params.image
        
        shapeX = params.image.shape[0]
        shapeY = params.image.shape[1]
        
        resized_image_opencv = cv.resize(params.image, (int(shapeY * params.factor_amplification), int(shapeX * params.factor_amplification)))
        params.image = resized_image_opencv
        
        print("Amplificam imaginea cu factorul : ")
        print(params.factor_amplification)
        
        
        params.num_pixels_width =  resized_image_opencv.shape[1] - shapeY
                              
        print("Din latime, extragem:")
        print(params.num_pixels_width)             
        
        
        params.image = decrease_width(params, params.num_pixels_width)
        
        params.num_pixels_height = resized_image_opencv.shape[0] - shapeX
        
        print("Din inaltime, extragem: ")
        print(params.num_pixels_height)
        
        resulted_image = decrease_height(params, params.num_pixels_height)
        
        params.image = originalImage 
        
        print(resulted_image.shape)
        return resulted_image
    
    
    elif params.resize_option == 'eliminaObiect':
        
        image_to_show = np.uint8(params.image[:, :, [0, 1, 2]])
        
        y, x, h, w = cv.selectROI("Image to choose rectangle", image_to_show, False, False)
    
        # cream masca pentru obiect (care se muta odata cu taierea pixelilor)
        params.image_obj = np.zeros((params.image.shape[0], params.image.shape[1]), np.uint8)
        
        print(x, y, w, h)
        
        resulted_image = delete_object(params, x, y, w, h)
        
        return resulted_image


    else:
        print('The option is not valid!')
        sys.exit(-1)