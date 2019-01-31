import os
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/data/iphone')

# import the necessary packages
from skimage.measure import _structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
from resizeimage import resizeimage
from PIL import Image

# ##formatage des images
# list_articles=os.listdir()
# list_images=[]
# list_width=[]
# list_height=[]
# for article in list_articles:
# 	list_images.append(Image.open(article,'r'))
# 	list_width.append(list_images[-1].size[0])
# 	list_height.append(list_images[-1].size[1])
# w=max(list_width)
# h=max(list_height)
# print(w,h)
# for k,image in enumerate(list_images):
# 	image=resizeimage.resize_contain(image,[w,h])
# 	image.save('modified_'+list_articles[k],image.format)
# 	
# ##formatage avec tkinter
# import tkinter as tk
# from PIL import Image, ImageTk
# root=tk.Tk()
# photo = Image.open('iphoneX.jpg')
# resolution = (160,160)
# img = ImageTk.PhotoImage(photo.resize(resolution))

##construction des indicateurs
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err
 
def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim.compare_ssim(imageA, imageB)
 
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
 
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")
 
	# show the images
	plt.show()
	
# ##example
# # load the images -- the original, the original + contrast,
# # and the original + photoshop
# original = cv2.imread("modified_iphoneX.jpg")
# contrast = cv2.imread("modified_iphoneX_unlocked.jpg")
# shopped = cv2.imread("modified_joconde.jpg")
#  
# #convert the images to grayscale
# original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
# contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
# shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)
# 
# # initialize the figure
# fig = plt.figure("Images")
# images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)
#  
# # loop over the images
# for (i, (name, image)) in enumerate(images):
# 	# show the image
# 	ax = fig.add_subplot(1, 3, i + 1)
# 	ax.set_title(name)
# 	plt.imshow(image, cmap = plt.cm.gray)
# 	plt.axis("off")
#  
# # show the figure
# plt.show()
#  
# # compare the images
# compare_images(original, original, "Original vs. Original")
# compare_images(original, contrast, "Original vs. Contrast")
# compare_images(original, shopped, "Original vs. Photoshopped")

##
def similarite(imageA,imageB):
	#on resize les images pour qu'elles aient les mêmes tailles
	list_articles=[imageA,imageB]
	list_images=[]
	list_width=[]
	list_height=[]
	new_images=[]
	for article in list_articles:
		list_images.append(Image.open(article,'r'))
		list_width.append(list_images[-1].size[0])
		list_height.append(list_images[-1].size[1])
	w=max(list_width)
	h=max(list_height)
	for k,image in enumerate(list_images):
		image=resizeimage.resize_contain(image,[w,h])
		image.save(str(k)+'.jpg',image.format)
		new_images.append(cv2.imread(str(k)+'.jpg'))
		new_images[k]=cv2.cvtColor(new_images[k], cv2.COLOR_BGR2GRAY)
	#calcul des indicateurs
	m = mse(new_images[0],new_images[1])
	s = ssim.compare_ssim(new_images[0],new_images[1])
	return(m,s)