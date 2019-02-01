from skimage import feature
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import numpy as np
from PIL import Image, ImageMath
from pylab import *
import scipy
import cv2


##
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/data/iphone')

def correction(n):#erreur dans la fonction de creation des contours (certaines valeurs ne sont pas égales à 0 ou 255, mais sont très proches, donc on corrige le tir
    if(255-n<n):
        return 255
    return 0

def contours(image):
    img = mpimg.imread(image)
    M = np.zeros((img.shape[0],img.shape[1]))
    M[:,:] = img[:,:,0]
    plt.imshow(M, cmap = plt.get_cmap('gray'))
    #---------- Apply Canny  ----------#
    edges = feature.canny(M, sigma=1)
    fig, ax = plt.subplots()
    ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
    ax.axis('off')
    plt.savefig("_contours"+image)
    #fig.show()
    #---on change les pixels noirs en blancs et inversement---#
    imgpil=Image.open("_contours"+image)
    image_array=np.asarray(imgpil)
    # ensemble=set()
    # for i in range(image_array.shape[0]):
    #     for j in range(image_array.shape[1]):
    #         for k in range(3):
    #             ensemble.add(image_array[i][j][k])
    # print(ensemble)
    
    contour_array=np.zeros(image_array.shape[:2],dtype='uint8')
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            contour_array[i][j]=255-correction(image_array[i][j][0])
    test=Image.fromarray(contour_array,'L')
    test.save("_contours"+image)
    test.show()


##
def image_to_contour(image,number):#number permet juste de numeroter l image
    # read image to array
    im = array(Image.open(image).convert('L'))
    # create a new figure
    figure()
    # show contours with origin upper left corner
    #contour(im, origin='image')
    fig=contour(im, levels=2, colors='black', origin='image') #levels=[255]
    axis('equal')
    axis('off')
    plt.savefig("contour_"+str(number)+".jpg")
    plt.close()

def formatage(tableau):
    n,m=tableau.shape
    new_tab=np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            new_tab[i][j]=tableau[i][j]/255
    return new_tab

def distance_hausdorff(image1,image2):
    image_to_contour(image1,1)
    image_to_contour(image2,2)
    contour1=formatage(cv2.imread("contour_1.jpg",0))
    contour2=formatage(cv2.imread("contour_2.jpg",0))
    return(scipy.spatial.distance.directed_hausdorff(contour1,contour2))
    
def symmetric_hausdorff(image1,image2):
    distance1=distance_hausdorff(image1,image2)
    distance2=distance_hausdorff(image2,image1)
    return(max(distance1,distance2))

##Superposition des deux images pour "voir la distance d'Hausdorff
im1 = Image.open("contour_1.jpg")
im2 = Image.open("contour_2.jpg")

out = ImageMath.eval("convert(min(a, b), 'L')", a=im1, b=im2)
out.save("result.png")