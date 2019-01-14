import pandas as pd
import numpy as np
import os
import sys
import pickle

os.chdir("C:\\Users\\quit7\\Desktop\\MOPSI\\code")
import text_processing

## Dataset 1

#Save all data

data = pd.read_csv("data_enpc_products_ng.csv")
# pickle.dump(data, open('.\\data\\alldata', 'wb'))

## Dataset 1

#Save data with tokenized and normalized text

data_processed = pickle.load(open('.\\data\\alldata', 'rb'))
data_processed = data_processed.dropna(subset=['product_name']) #remove unnamed products
data_processed.product_name = data_processed.product_name.apply(tokenize)
data_processed.product_name = data_processed.product_name.apply(normalize)
# pickle.dump(data_processed, open('.\\data\\data_processed','wb'))      


## Merge the datasets

import stringdist  #for the Levenshtein distance

data = pd.read_csv("enpc_raw_data_products_ng.csv")
data = data.drop_duplicates('ID')
data2 = pd.read_csv("data_enpc_products_ng.csv")
data2 = data2.drop_duplicates('sku')

data3 = pd.merge(left=data2,right=data,left_on=['sku'],right_on=['ID'],how='outer')

def mergeID(row):
    if type(row['sku'])!=str:
        return row['ID']
    return row['sku']
    
data3['sku'] = data3.apply(mergeID,axis=1) #Merge products sku
data3 = data3.drop('ID',axis=1) #Delete column 'ID'

def mergeNames(row):
    names = [row['product_name'],row['Name']]
    if type(names[0])!=str:
        return names[1]
    if type(names[1])!=str:
        return names[0]
    
    #If names are differents, we use the levenshtein distance to measure the difference
    if names[0]!=names[1]:
        m = min(len(names[0]),len(names[1]))
        dist = stringdist.levenshtein_norm(names[0][:m],names[1][:m])
        if dist>0.3: 
            return float('NaN')
    return names[0]
    
data3['product_name'] = data3.apply(mergeNames,axis=1) #Merge products name
data3 = data3.dropna(subset=['product_name'])
data3 = data3.drop('Name',axis=1) #Delete column 'Name'

data3.to_csv(".\\data\\joined_dataset.csv")
# pickle.dump(data3, open('.\\data\\joined_data', 'wb'))

##

reader = pd.read_csv(".\\data\\joined_dataset.csv", chunksize=300000, encoding = "ISO-8859-1")

def processDescription(desc):
    if type(desc)==str:
        text = desc
        text = text_processing.tokenize(text)
        text = text_processing.normalize(text)
        return text

def processCategories(cat):
    if type(cat)==str:
        cat = cat.split(', ')
        if cat[0] == 'Root Category':
            cat = cat[1:]
        return cat


k = 0
for chunk in reader:
    print('Processing chunk n°',k)
    chunk.Description = chunk.Description.apply(processDescription)
    print('Description processing done')
    chunk.Categories = chunk.Categories.apply(processCategories)
    print('Categories processing done')
    chunk.product_name = chunk.product_name.apply(processDescription)
    print('Product name processing done')
    chunk.to_csv(".\\data\\processed_data_"+str(k)+".csv",encoding = "ISO-8859-1")
    k+=1


## Get categories


data = pd.read_csv("enpc_raw_data_products_ng.csv")
data = data[['Categories','ID']]
data = data.dropna(subset=['Categories','ID'])

def processCategories2(cat):
    cat = cat.split(', ')
    if cat[0] == 'Root Category':
        cat = cat[1:]
    return cat

data.Categories = data.Categories.apply(processCategories2)



## Get categories 1

cat1 = []
min = 1
max = 23
for index,row in data.iterrows():
    if row['Categories'][0] not in cat1:
        cat1 += [row['Categories'][0]]

        
## Get categories 2

cat2 = [[] for k in range(len(cat1))]

for index,row in data.iterrows():
    if index%10000==0:
        print(index)
    a = row['Categories']
    idx = cat1.index(a[0])
    if len(a)>1 and (a[1] not in cat2[idx]):
        cat2[idx] += [a[1]]


## Get categories 3

cat1 = ['Fashion', 'Grocery', 'Health & Beauty', 'Home & Office', 'Computing', 'Sporting Goods', 'Phones & Tablets', 'Gaming', 'Garden & Outdoors', 'Baby Products', 'Electronics', 'Books', 'Automobile', 'Toys & Games', 'Pet Supplies', 'Musical Instruments', 'Miscellaneous', 'Industrial & Scientific', 'Services', 'Livestock']


data = pd.read_csv("enpc_raw_data_products_ng.csv")
data = data['Categories']
data = data.dropna()


def processCategories3(cat):
    cat = cat.split(', ')
    if cat[0] == 'Root Category':
        if len(cat)>4:
            return cat[1:4]
        return float('NaN')
    if len(cat)>2:
        return cat[0:3]
    return float('NaN')

data2 = data.apply(processCategories3)
data2 = data2.dropna()

cat3 = [[[] for i in range (len(cat2[k]))] for k in range(len(cat1))]

for index,row in data2.iteritems():
    if index%10000==0:
        print(index)
    a = row
    idx1 = cat1.index(a[0])
    idx2 = cat2[idx1].index(a[1])
    if a[2] not in cat3[idx1][idx2]:
        cat3[idx1][idx2] += [a[2]]
        
# pickle.dump(cat3, open('.\\data\\category3', 'wb'))

## Get Category 4

def processCategories4(cat):
    cat = cat.split(', ')
    if cat[0] == 'Root Category':
        if len(cat)>5:
            return cat[1:5]
        return float('NaN')
    if len(cat)>3:
        return cat[0:4]
    return float('NaN')
    
data3 = data.apply(processCategories4)
data3 = data3.dropna()

cat4 = [[[[] for j in range (len(cat3[k][i]))] for i in range (len(cat2[k]))] for k in range(len(cat1))]

for index,row in data3.iteritems():
    if index%10000==0:
        print(index)
    a = row
    idx1 = cat1.index(a[0])
    idx2 = cat2[idx1].index(a[1])
    idx3 = cat3[idx1][idx2].index(a[2])
    if a[3] not in cat4[idx1][idx2][idx3]:
        cat4[idx1][idx2][idx3] += [a[3]]

# pickle.dump(cat4, open('.\\data\\category4', 'wb'))

