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
import imutils


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
# Open an Image
def open_image(path):
    newImage = Image.open(path)
    return newImage

def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image
    
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
      return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def save_image(image, path):
    image.save(path, 'png')

def convert_to_red(image_adress):
    image=open_image(image_adress)
    # Get size
    width, height = image.size
    #Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    # Transform to grayscale
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)
            #Transform to red
            if pixel==(0,0,0):
                pixels[i,j]=(255,0,0)
            else:
                pixels[i,j]=(255,255,255)
    # Return new image
    save_image(new,"contour_red.jpg")
    
def convert_to_blue(image_adress):
    image=open_image(image_adress)
    # Get size
    width, height = image.size
    #Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()
    # Transform to grayscale
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)
            #Transform to red
            if pixel==(0,0,0):
                pixels[i,j]=(0,0,255)
            else:
                pixels[i,j]=(255,255,255)
    # Return new image
    save_image(new,"contour_blue.jpg")

def superposition():
    convert_to_blue("contour_1.jpg")
    background = Image.open("contour_blue.jpg")
    convert_to_red("contour_2.jpg")
    overlay = Image.open("contour_red.jpg")
    
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    
    new_img = Image.blend(background, overlay,0.5)
    new_img.save("new.png","PNG")

superposition()