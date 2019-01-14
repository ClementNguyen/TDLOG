import pandas as pd
import numpy as np
import os
import sys
import nltk 
from nltk.corpus import stopwords

os.chdir(r"C:\Users\Wissam\Desktop\IMI\MOPSI\Similarity")
import text_processing


# Sample of product categories
products = [   ['Fashion', 'Wallets'],
    ['Fashion', 'Watches'],
    ['Fashion', 'Sunglasses'],
    ['Fashion', 'Luggage'],
    ['Fashion', 'Backpacks'],
    ['Fashion', 'Shoes'],
    ['Fashion', 'Shirts'],
    ['Fashion', 'Pants'],
    ['Fashion', 'Dresses'],
    ['Fashion', 'Skirts'],
    ['Fashion', 'Belts'],
    #Grocery
    #Health & Beauty
    ['Home & Office', 'Clocks'],
    ['Home & Office', 'Mirrors'],
    ['Home & Office', 'Painting'],
    ['Home & Office', 'Refrigerators'],
    ['Computing', 'Laptops'],
    ['Computing', 'Desktops'],
    ['Computing', 'External Hard Drives'],
    ['Computing', 'USB Flash Drives'],
    ['Computing', 'Printers'],
    ['Computing', 'Keyboards'],
    #Sporting Goods
    ['Phones & Tablets', 'Cases'],
    ['Phones & Tablets', 'SD Cards'],
    ['Phones & Tablets', 'Screen Protectors'],
    #Gaming
    ['Garden & Outdoors', 'Chairs'],
    ['Garden & Outdoors', 'Plants'],
    ['Garden & Outdoors', 'Grills'],
    ['Baby Products', 'Diaper Bags'],
    ['Electronics', 'Headphones'],
    ['Electronics', 'Remote Controls'],
    ['Electronics', 'Sound Bars'],
    ['Electronics', 'Gas Heaters'],
    #Books
    #Automobile
    ['Toys & Games', 'Puzzles'],
    ['Toys & Games', 'Board Games'],
    #Pet Supplies
    ['Musical Instruments', 'Keyboards & MIDI'] ]
    #Miscellaneous
    #Industrial & Scientific
    #Services  
    #Livestock

# Get only the second category
products2 = []
for i in range(len(products)):
    products2 += [products[i][1]]
    
    
def createProductsSample(products):
    """
    Create a dataset of products from given categories.
    """
    data = pd.read_csv("enpc_raw_data_products_ng.csv")
    data = data[['Categories','Name','Description','RetailPrice']]
    data = data.dropna()
    
    def processCategories(cat):
        """
        Transform the string "['Root Category','Cat1',...]" into a list ['Cat1',...]
        """
        cat = cat.split(', ')
        if cat[0] == 'Root Category':
                return cat[1:]
        return cat
    data.Categories = data.Categories.apply(processCategories)
    
    def wantedProducts(cat):
        """
        Check if the product is in a wanted category
        """
        for i in range (len(products)):
            if (cat[0]==products[i][0]):
                if (products[i][1] in cat):
                    return products[i][1]
        return float('NaN')
        
    data.Categories = data.Categories.apply(wantedProducts)
    data = data.dropna(subset=['Categories'])
    
    idx = 0
    def processDescription(desc):
        """
        Process products' description
        """
        global idx
        idx += 1
        if (idx%10000==0):
            print(idx)
        if type(desc)==str:
            text = desc
            text = text_processing.tokenize(text)
            text = text_processing.normalize(text)
            return text
    
    data.Description = data.Description.apply(processDescription)
    data.Name = data.Name.apply(processDescription)
    
    stopwords_ = set(stopwords.words('english'))
    idx = 0 
    def remove_stopwords(words):
        """
        Remove stopwords
        """
        global idx
        idx += 1
        if (idx%10000==0):
            print(idx)
        new_words = []
        for word in words:
            if word not in stopwords_:
                new_words.append(word)
        return new_words
    
    data.Name = data.Name.apply(remove_stopwords)
    data.Description = data.Description.apply(remove_stopwords)
    # Save resulting dataset
    data.to_csv(".\\ml\\similarity\\products_sample.csv")


def createSimilarityTrainingSet():
    """
    Create a dataset of index pair of the dataframe product_sample and the similarity between the two products.
    The number of similar products and not similar products are equal.
    """
    data = pd.read_csv(".\\ml\\similarity\\products_sample.csv")
    data = data['Categories']
    
    print('Processing similar products...')
    similar_products = []
    for i in range(len(products2)):
        data2 = data[data==products2[i]]
        nb_it = min(20,20000//len(data2))
        for j in range(nb_it):
            data2 = data2.iloc[np.random.permutation(len(data2))]
            data3 = data2.iloc[np.random.permutation(len(data2))]
            index1 = data2.index.tolist()
            index2 = data3.index.tolist()
            for k in range(len(index1)):
                similar_products += [ [index1[k],index2[k]] ]
    
    print('Processing unsimilar products...')
    unsimilar_products = []
    while (len(unsimilar_products)<len(similar_products)):
        data2 = data.iloc[np.random.permutation(len(data))]
        data3 = data2.iloc[np.random.permutation(len(data))]
        index1 = data2.index.tolist()
        index2 = data3.index.tolist()
        for i in range(len(index1)):
            if (data2.iloc[i]!=data3.iloc[i]):
                unsimilar_products += [ [index1[i],index2[i]] ]
    del data2, data3
    unsimilar_products = rd.sample(unsimilar_products,len(similar_products))
    
    res = pd.concat([pd.Series(similar_products+unsimilar_products),pd.Series(len(similar_products)*[1]+len(unsimilar_products)*[0])],axis=1,keys=['Index','Similarity'])
    res = res.iloc[np.random.permutation(len(res))]
    res.to_csv(".\\ml\\similarity\\similarity_training_set.csv",index=False, encoding='utf-8')
        

if __name__ == '__main__':
    
    createProductsSample(products)
    
    createSimilarityTrainingSet()