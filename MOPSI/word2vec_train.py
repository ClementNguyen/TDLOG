import pandas as pd
import numpy as np
import os
import gensim
import utils
from gensim.models import Word2Vec,doc2vec
from sklearn.utils import shuffle
import sys
import random

path="D:/Sasha/Documents/ENPC/IMI/MOPSI/github/TDLOG/MOPSI"
sys.path.append('D:/Sasha/Documents/ENPC/IMI/MOPSI/github/ressources')
os.chdir(path)
import text_processing

def createTrain(data):
    """
    Create a set of list of words to train a Word2Vec model
    """
    train = []
    for index,row in data.iterrows():
        train.append(row['product_name']+row['Description'])
    return train
    
def strToList(x):
    if type(x)==str:
        return x[2:-2].split("', '")
    
def trainWord2Vec():
    """
    Create, train, save Word2Vec model
    To load model:
    w2v_model = Word2Vec.load(".\ml\word2vec\w2v_model")
    """
    model = gensim.models.Word2Vec(size=160, window=5, min_count=2, workers=10)
        
    for i in range(6):
        print("Chunk "+str(i)+"...")
        data = pd.read_csv(data2.processed.csv,encoding = "ISO-8859-1")#".\\data\\processed_data_"+str(i)+".csv"
        data = data[['product_name','Description']]
        data = data.dropna()
        data.product_name = data.product_name.apply(strToList)
        data.Description = data.Description.apply(strToList)
        
        train = createTrain(data)
        del data
        print("Training...")
        update_vocab = True
        if (i==0):
            update_vocab = False
        model.build_vocab(train,update=update_vocab)
        model.train(train,total_examples=len(train),epochs=10)
    model.save(".\\ml\\word2vec\\w2v_model")
    

        
def createTaggedDocuments(data):
    """
    Create a list of Tagged Documents to train a Doc2Vec model
    """
    train = []
    for index,row in data.iterrows():
        if (index%10000==0):
            print(index)
        train.append(doc2vec.TaggedDocument(row['Description'],tags=[row['ID']]))
    return train        

def trainDoc2Vec():
    """
    Create, train, save Doc2Vec model
    To load model:
    d2v_model = doc2vec.Doc2Vec.load(".\ml\word2vec\d2v_model")
    """
    model = gensim.models.doc2vec.Doc2Vec(vector_size=160, min_count=1, window=1)
    data = pd.read_csv("D:/Sasha/Documents/ENPC/IMI/MOPSI/github/ressources/data2_processed.csv")
    data = data[['ID','Name','Description']]
    data.Name = data.Name.apply(text_processing.strToList)
    data.Description = data.Description.apply(text_processing.strToList)

    train = createTaggedDocuments(data)

    del data
    print("Building vovabulary...")
    model.build_vocab(train)
    print("Training...")
    for epoch in range(10):
        print('epoch n°',epoch)
        model.train(shuffle(train),total_examples=len(train),epochs=1)
        model.alpha -= 0.002
        model.min_alpha = model.alpha
    model.save("D:/Sasha/Documents/ENPC/IMI/MOPSI/github/ressources/d2v_model")
    


if __name__ == '__main__':
    
    # Create, train, save Word2Vec model
    #trainWord2Vec()
    # Create, train, save Doc2Vec model
    trainDoc2Vec()
