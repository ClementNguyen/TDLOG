import pandas as pd
import os
import nltk
from gensim.models import Word2Vec, doc2vec
from scipy import spatial
import matplotlib.pyplot as plt
import numpy as np
import random

path="D:\\Sasha\\Documents\\ENPC\\IMI\\MOPSI\\github\\ressources"
os.chdir(path)
data2 = pd.read_csv("data2_processed.csv")
d2v_model = doc2vec.Doc2Vec.load("d2v_model")

##comparaison avec doc2vec
def distance_d2v(index1,index2):
    vect1=d2v_model.docvecs[data2.loc[index1,'ID']]
    vect2=d2v_model.docvecs[data2.loc[index2,'ID']]
    return abs(spatial.distance.cosine(vect1, vect2))

# def descriptionSimilarity2(index1,index2,data2):
#     desc1 = data2.loc[index1,'Description']
#     desc2 = data2.loc[index2,'Description']
#     vect1 = d2v_model.infer_vector(desc1)
#     vect2 = d2v_model.infer_vector(desc2)
#     return abs(spatial.distance.cosine(vect1, vect2))
##Accuracy
nb_data=data2.shape[0]
nmax=200

def index_of_category(category):
    index_product=[]
    for k in range(nb_data):
        if category in data2.loc[k,"Categories"]:
            index_product.append(k)
    return(index_product)

index_product=index_of_category("['Gaming', 'Playstation', 'PlayStation 4', 'Consoles']")
#index_product=index_of_category("['Phones & Tablets', 'Mobile Phones', 'Smartphones', 'Android Phones']")
#index_product=index_of_category("['Home & Office', 'Home & Kitchen', 'Kitchen & Dining', 'Small Appliances', 'Microwave Ovens']")


def vecteur_moyen(index_product):
    vector_categorie=d2v_model.docvecs[index_product[0]]
    for k in range(1,len(index_product)):
        vector_categorie+=d2v_model.docvecs[index_product[k]]
    return(vector_categorie/len(index_product))


def test_accuracy_in_category():
    mean=0
    n=min(len(index_product),nmax)
    l_distances=[]
    for j in range(n):
        for k in range(n):
            l_distances.append(distance_d2v(index_product[j],index_product[k]))
    return np.mean(l_distances),np.median(l_distances)
    
def test_accuracy_outside_category(product_ref):
    liste_distances=[]
    n=min(len(index_product),nmax)
    for k in range(n):
        liste_distances.append(distance_d2v(product_ref,index_product[k]))
    return min(liste_distances), np.mean(liste_distances), np.median(liste_distances)


m_inside,median_inside=test_accuracy_in_category()

def graph1(nb_products):#graphe qui représente la similarité moyenne de nb_products produits extérieurs à la catégorie concernée)
    l_mean=[]
    l_min=[]
    l_median=[]
    resu=0
    compteur=0
    for k in range(nb_products):
        if k not in index_product:
            compteur+=1
            resu=test_accuracy_outside_category(k)
            l_min.append(resu[0])
            l_mean.append(resu[1])
            l_median.append(resu[2])
    
    plt.figure()
    #plt.plot(np.arange(compteur),l_min)
    #plt.plot(np.arange(compteur),l_mean)
    plt.plot(np.arange(compteur),l_median)
    #m_inside=test_accuracy_in_category()
    #plt.plot([0,compteur-1],[m_inside,m_inside])
    plt.plot([0,compteur-1],[median_inside,median_inside])
    #plt.legend(["min","mean","median","mean_inside","median_inside"])
    plt.legend(["median","median_inside"])
    plt.show()

graph1(150)

##Images
# import urllib.request
# urllib.request.urlretrieve('https://ng.jumia.is/MjkSuqBBIQ1fiMCMp2jEv-Cb2Po=/fit-in/500x500/filters:fill(white)/product/89/28679/1.jpg?0368',"test.jpg")
# set_categories=set()
# for k in range(200):
#     set_categories.add(data2.loc[k,"Categories"])
# print(set_categories)

for k in range(nb_data):
    if "microwave" in data2.loc[k,"Name"]:
        print(k)