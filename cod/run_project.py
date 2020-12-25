"""
    PROIECT
    REDIMENSIONEAZA IMAGINI.
    Implementarea a proiectului Redimensionare imagini
    dupa articolul "Seam Carving for Content-Aware Iamge Resizing", autori S. Avidan si A. Shamir
    
    Badea Adrian Catalin, grupa 334, anul III, FMI
    
"""


from parameters import *
from resize_image import *
import matplotlib.pyplot as plt
import cv2 as cv


image_name = '../data/arcTriumf.jpg'
params = Parameters(image_name)



params = Parameters(image_name)
params.method_select_path = 'programareDinamica'
resized_image = resize_image(params)


'''
# Pentru celelalte metode :

params = Parameters(image_name)
params.method_select_path = 'greedy'
resized_image = resize_image(params)

cv.imwrite('lac_greedy.png', resized_image)


params = Parameters(image_name)
params.method_select_path = 'aleator'
resized_image = resize_image(params)

cv.imwrite('lac_aleator.png', resized_image)

'''




# Imaginea redimensionata cu openCV

c = cv.resize(params.image, (resized_image.shape[1], resized_image.shape[0]))

cv.imwrite('arcTriumf_opencv.png', c)


plt.subplot(1, 3, 2)
plt.imshow(np.uint8(resized_image_opencv[:, :, [2, 1, 0]]))
plt.xlabel('OpenCV')



# Imaginea originala
f, axs = plt.subplots(2, 2, figsize=(15, 15))
plt.subplot(1, 3, 1)
plt.imshow(np.uint8(params.image[:, :, [2, 1, 0]]))
plt.xlabel('original')

# Imaginea folosind content-aware resizing

plt.subplot(1, 3, 3)
plt.imshow(resized_image[:, :, [2, 1, 0]])
plt.xlabel('my result')
plt.show()



cv.destroyAllWindows()



