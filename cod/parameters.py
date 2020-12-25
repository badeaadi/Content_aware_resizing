"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Iamge Resizing", autori S. Avidan si A. Shamir
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
    
"""

import cv2 as cv
import sys
import numpy as np


class Parameters:

    def __init__(self, image_name):
        self.image_name = image_name
        self.image = cv.imread(image_name)
        
       
        if self.image is None:
            print('The image name %s is invalid.' % self.image_name)
            sys.exit(-1)
        self.image = np.float32(self.image)
        
                
        # seteaza optiunea de redimenionare
        # micsoreazaLatime, micsoreazaInaltime, amplificaContinut, eliminaObiect
        self.resize_option = 'amplificaContinut'
  
        # numarul de pixeli pe latime
        self.num_pixels_width = 50
        # numarul de pixeli pe inaltime
        self.num_pixels_height = 100
        
        if self.resize_option == 'amplificaContinut':
            # factorul de amplificare, mai mare ca 1
            self.factor_amplification = 1.4
            
        # metoda pentru alegerea drumului
        # aleator, greedy, programareDinamica
        self.method_select_path = 'programareDinamica'
        
        # afiseaza drumul eliminat
        self.show_path = True
        # culoarea drumului de afisat
        self.color_path = (0, 0, 255)
   
        