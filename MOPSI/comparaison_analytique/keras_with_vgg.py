from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from sklearn.cluster import KMeans

import numpy as np

model = VGG16(weights='imagenet', include_top=False)
#model.summary()
##
import os
os.chdir("D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data")

##

img_path = 'D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data\\dogs\\1.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_data = image.img_to_array(img)
img_data = np.expand_dims(img_data, axis=0)
img_data = preprocess_input(img_data)

vgg16_feature = model.predict(img_data)

#print(vgg16_feature.shape)

##clustering
# path="D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data\\images"
# os.chdir(path)
# subdir=os.listdir('.')
# vgg16_feature_list = []
# 
# for idx, dirname in enumerate(subdir):
#     print(idx)
#     if(idx==10):
#         break
#     # get the directory names, i.e., 'dogs' or 'cats'
#     filenames=os.listdir(os.path.join(path,dirname))
#     os.chdir(filenames)
#     list_images=os.listdir('.')
#     for i, fname in enumerate(list_images):
#         # process the files under the directory 'dogs' or 'cats'
#         # ...
#         
#         img = image.load_img(fname, target_size=(224, 224))
#         img_data = image.img_to_array(img)
#         img_data = np.expand_dims(img_data, axis=0)
#         img_data = preprocess_input(img_data)
# 
#         vgg16_feature = model.predict(img_data)
#         vgg16_feature_np = np.array(vgg16_feature)
#         vgg16_feature_list.append(vgg16_feature_np.flatten())
#         
# vgg16_feature_list_np = np.array(vgg16_feature_list)
# kmeans = KMeans(n_clusters=idx, random_state=0).fit(vgg16_feature_list_np)
# sol=kmeans.cluster_centers_

##
path="D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data\\iphone"
os.chdir(path)

def test_similarite_RN(image1,image2):#réseau de neurones = RN
    vector1=vectorize(image1)
    vector2=vectorize(image2)
    return vector1.dot(vector2)/(np.sqrt(vector1.dot(vector1))*np.sqrt(vector2.dot(vector2)))

def vectorize(img_path):
    #img_path = 'D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data\\dogs\\'+str(index)+'.jpg'
    img = image.load_img(img_path, target_size=(224, 224))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    
    vgg16_feature = model.predict(img_data)
    return vgg16_feature.flatten()

##
# path="D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\data\\essai"
# os.chdir(path)
# subdir=os.listdir('.')
# for idx, dirname in enumerate(subdir):
#     filesname=os.path.join(path,dirname)
#     print(filesname)
