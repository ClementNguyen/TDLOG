import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/python/MOPSI/comparaison_analytique')
import hausdorff_test as haus
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/python/MOPSI/comparaison_analytique')
import keras_with_vgg as ker
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/python/MOPSI/comparaison_analytique')
import mse_ssim as ms
os.chdir('D:/Sasha/Documents/ENPC/IMI/MOPSI/data/iphone')#dossier contenant les images

def comparaison_analytique(image1,image2):
    indicateurs=[haus.symmetric_hausdorff(image1,image2)[0],ker.test_similarite_RN(image1,image2)]
    MS=ms.similarite(image1,image2)
    indicateurs.append(MS[0])
    indicateurs.append(MS[1])
    print("distance d'hausdorff = ", indicateurs[0])
    print("distance cosinus via RN = ", indicateurs[1])
    print("mse, ssim = ", indicateurs[2],indicateurs[3])
    return(indicateurs)

def graph_comparaison(direction):#mettre le dossier contenant les images en paramètre
    os.chdir(direction)
    liste_dir=os.listdir()
    liste_names=["Distance d'hausdorff","Distance cosinus avec RN","MSE","SSIM"]
    graphs=[[],[],[],[]]
    for dir in liste_dir[1:] :
        if dir not in ["contour_1.jpg","contour_2.jpg","0.jpg"]:
            resu=comparaison_analytique(liste_dir[0],dir)
            for k in range(4):
                graphs[k].append(resu[k])
    for k in range(4):
        plt.figure(k)
        plt.title(liste_names[k])
        plt.plot(np.arange(len(graphs[k])),graphs[k])
    plt.show()