import pandas as pd
import os
import nltk
from gensim.models import Word2Vec, doc2vec
from scipy import spatial
import matplotlib.pyplot as plt
import numpy as np

path="D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\github\\ressources"
os.chdir(path)
data2 = pd.read_csv("data2_processed.csv")
d2v_model = doc2vec.Doc2Vec.load("d2v_model")

##comparaison d'images avec doc2vec
def descriptionSimilarity(index1,index2,data2):
    desc1 = data2.loc[index1,'Description']
    desc2 = data2.loc[index2,'Description']
    vect1 = d2v_model.infer_vector(desc1)
    vect2 = d2v_model.infer_vector(desc2)
    return abs(spatial.distance.cosine(vect1, vect2))

##Accuracy
nb_data=data2.shape[0]
index_product=[]
categorie="['Gaming', 'Playstation', 'PlayStation 4', 'Consoles']"
for k in range(nb_data):
    if "['Gaming', 'Playstation', 'PlayStation 4', 'Consoles']" in data2.loc[k,"Categories"]:
        index_product.append(k)


def test_accuracy_in_category(product_ref,nb):
    nb=min(nb,len(index_product))
    mean=0
    for k in range(nb):
        mean+=descriptionSimilarity(product_ref,index_product[k],data2)
    mean=mean/nb
    return mean
    
def test_accuracy_outside_category(product_ref,nb_comparaisons):
    distance_min=1
    mean=0
    n=min(len(index_product),nb_comparaisons)
    for k in range(n):
        distance_min=min(distance_min,descriptionSimilarity(product_ref,index_product[k],data2))
        mean+=descriptionSimilarity(product_ref,index_product[k],data2)
    return distance_min, mean/n

def graph1(nb_products):#graphe qui représente la similarité moyenne de nb_products produits extérieurs à la catégorie concernée
    nb_products=min(nb_products,len(index_product))
    means=[]
    means_similar=[]
    low_bounds=[]
    low_bounds_similar=[]
    resu=0
    compteur=0
    for k in range(nb_products):
        if k not in index_product:
            compteur+=1
            resu=test_accuracy_outside_category(k,50)
            low_bounds.append(resu[0])
            means.append(resu[1])
            
            resu=test_accuracy_in_category(index_product[k],50)
            means_similar.append(resu)
            
    plt.plot(np.arange(compteur),means)
    plt.plot(np.arange(compteur),low_bounds)
    plt.plot(np.arange(compteur),means_similar)
    plt.show()


##Images
# import urllib.request
# urllib.request.urlretrieve('https://ng.jumia.is/MjkSuqBBIQ1fiMCMp2jEv-Cb2Po=/fit-in/500x500/filters:fill(white)/product/89/28679/1.jpg?0368',"test.jpg")
