import os
import pandas as pd
import numpy as np
import pickle
from gensim.models import Word2Vec, doc2vec
from scipy import spatial
from collections import Counter
import time
#back-end
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

path = "C:\\Users\\quit7\\Desktop\\MOPSI\\code"
os.chdir(path)

def strToList(x):
    """
    Transform "['a', 'b']" into ['a', 'b']
    """
    if type(x)==str:
        return x[2:-2].split("', '")

data = pd.read_csv(".\\data\\data2_processed.csv")
data = data.drop(['SmallImage','currency'], axis=1)
#data.Name = data.Name.apply(strToList)
#data.Description = data.Description.apply(strToList)
#data.Categories = data.Categories.apply(strToList)

w2v_model = Word2Vec.load(".\ml\word2vec\w2v_model")
vocab = w2v_model.wv.vocab
index2word_set = set(w2v_model.wv.index2word)

#d2v_model = doc2vec.Doc2Vec.load(".\ml\word2vec\d2v_model")


def avg_feature_vector(words):
  num_features = 160
  feature_vec = np.zeros((num_features, ), dtype='float32')
  n_words = 0
  for word in words:
      if word in index2word_set:
          n_words += 1
          feature_vec = np.add(feature_vec, w2v_model[word])
  if (n_words > 0):
      feature_vec = np.divide(feature_vec, n_words)
  return feature_vec
  
def w2vScores(text1,text2):
  text1_afv = avg_feature_vector(text1)
  text2_afv = avg_feature_vector(text2)
  try:
      text_sim = abs(1 - spatial.distance.cosine(text1_afv, text2_afv))
  except:
      text_sim = 0
  if (np.isnan(text_sim)):
    text_sim = 0
  return text_sim      
      
def nameDist(name1,name2):
  return w2vScores(name1,name2)
  
def descDist(desc1,desc2):
  vect1 = d2v_model.infer_vector(desc1)
  vect2 = d2v_model.infer_vector(desc2)
  try:
      text_sim = abs(1 - spatial.distance.cosine(vect1, vect2))
  except:
      text_sim = 0
  if (np.isnan(text_sim)):
    text_sim = 0
  return text_sim   
  
def distByID(id1,id2):
  name1 = data[data['ID']==id1]['Name'].values[0]
  name2 = data[data['ID']==id2]['Name'].values[0]
  return nameDist(name1,name2)

def findRecommendationsV1(id):
    
    product = data[data['ID']==id]
    
    product_cat_str = data[data['ID']==id]['Categories'].values[0]
    similar = data[data['Categories']==product_cat_str].sample(5)
    similar = similar['ID'].values
    
    product_cat_list = strToList(product_cat_str)
    product_cat_list = product_cat_list[:-1]
    complementary_cat = ', '.join("'{0}'".format(cat) for cat in product_cat_list)
    complementary = data[data['Categories'].str.contains(complementary_cat)]
    complementary = complementary[complementary['Categories']!=product_cat_str].sample(5)
    complementary = complementary['ID'].values
    
    res = [[],[]]
    for i in range(len(similar)):
        res[0].append({'ID': similar[i]})
    for i in range(len(complementary)):
        res[1].append({'ID': complementary[i]})
    return res
    
def findRecommendations(id):
  #id = 'CA099FA0MYDUINAFAMZ'
  product = data[data['ID']==id]
  product_name = strToList(product['Name'].values[0])
  product_desc = strToList(product['Description'].values[0])
  T0 = time.clock()
  product_cat_str = product['Categories'].values[0]
  print(product_cat_str)
  product_cat = strToList(product_cat_str)

  df_similar = data[data['Categories']==product_cat_str]
  df_similar = df_similar[df_similar['Name']!=product['Name'].values[0]]
  df_similar = df_similar.sample(min(1000,len(df_similar)))
  df_similar.Name = df_similar.Name.apply(strToList)
  all_names = df_similar['Name'].sample(min(len(df_similar),1000)).sum()
  common_words = Counter(all_names)
  common_words = [x[0] for x in common_words.most_common(5)]
  
  print("Most frequent words: ", common_words)
  print("T0: ", time.clock()-T0)
  
  all_dist = []
  mean_dist = 0
  for index,row in df_similar.iterrows():
    dist = nameDist(product_name,row['Name'])
    all_dist.append((dist, row['ID']))
    mean_dist += dist
  print("T1: ", time.clock()-T0)
  mean_dist = mean_dist/len(df_similar)
  all_dist = sorted(all_dist)
  similar = all_dist[-5:]
  similar_above_mean = [x[1] for x in similar if x[0]>0.5]
  similar = [x[1] for x in similar]
  print('mean dist:',mean_dist)
  
  complementary = []
  if (len(similar_above_mean)<5):
    if (len(similar_above_mean)==0):
      similar_above_mean = similar
    if (len(df_similar)>100):
      n = len(all_dist)//4
      complementary = [x[1] for x in all_dist[n:n+5]]
  
  if (len(complementary)==0):
    
    product_cat_list = strToList(product_cat_str)
    product_cat_list = product_cat_list[:-1]
    complementary_cat = ', '.join("'{0}'".format(cat) for cat in product_cat_list)
    all_complementary = data[data['Categories'].str.contains(complementary_cat)]
    all_complementary = all_complementary[all_complementary['Categories']!=product_cat_str]
    all_complementary.Name = all_complementary.Name.apply(strToList)
    complementary_cat_values = all_complementary['Categories'].unique()
    
    for cat in complementary_cat_values:
      if len(complementary)<15:
        
        df_complementary_cat = all_complementary[all_complementary['Categories']==cat]
        all_names_cat = df_complementary_cat['Name'].sample(min(len(df_complementary_cat),1000)).sum()
        common_words_cat = Counter(all_names_cat)
        common_words_cat = [x[0] for x in common_words_cat.most_common(5)]
        common_words_dist = w2vScores(common_words,common_words_cat)
        
        print('Category :', cat)
        print("Most frequent words: ", common_words_cat)
        print('Frequent words dist: ', common_words_dist)
        
        if (common_words_dist<0.40 or mean_dist<0.3 or len(product_cat)<4):
          if (common_words_dist < 0.40):
            best_dist = [0,0]
          else:
            best_dist = [1,0]
          for index, row in df_complementary_cat.iterrows():
            dist = nameDist(product_name,row['Name'])
            if ((common_words_dist<0.40 and dist>best_dist[0]) or (common_words_dist>0.40 and dist<best_dist[0])):
              best_dist = [dist,row['ID']]
          
          # best_product = data[data['ID']==best_dist[1]]
          # best_product_desc = strToList(best_product['Description'].values[0])
          # print(best_product['Name'])
          # print("infer vec dist: ", descDist(best_product_desc,product_desc))
          # print("avg vect dist: ", nameDist(best_product_desc,product_desc))
          
          if (best_dist[0]<0.85):
            complementary.append(best_dist[1])
    print("T3: ", time.clock()-T0)
    
    k=0  
    while (len(complementary)<5):
      k+=1
      product_cat_list2 = product_cat_list[:-1]
      complementary_cat2 = ', '.join("'{0}'".format(cat) for cat in product_cat_list2)
      all_complementary = data[data['Categories'].str.contains(complementary_cat2)]
      all_complementary = all_complementary[~all_complementary['Categories'].str.contains(complementary_cat)]
      all_complementary.Name = all_complementary.Name.apply(strToList)
      complementary_cat_values2 = all_complementary['Categories'].unique()
      
      for cat in complementary_cat_values2:
        if (len(complementary)<15):
        
          df_complementary_cat = all_complementary[all_complementary['Categories']==cat]
          all_names_cat = df_complementary_cat['Name'].sample(min(len(df_complementary_cat),1000)).sum()
          common_words_cat = Counter(all_names_cat)
          common_words_cat = [x[0] for x in common_words_cat.most_common(5)]
          common_words_dist = w2vScores(common_words,common_words_cat)
          
          print('Category :', cat)
          print("Most frequent words: ", common_words_cat)
          print('Frequent words dist: ', common_words_dist)
          
          if (common_words_dist<0.45 or len(product_cat)-k<4):
            if (common_words_dist < 0.40):
              best_dist = [0,0]
            else:
              best_dist = [1,0]
            df_complementary_cat = all_complementary[all_complementary['Categories']==cat]
            df_complementary_cat = df_complementary_cat.sample(min(200,len(df_complementary_cat)))
            for index, row in df_complementary_cat.iterrows():
              dist = nameDist(product_name,row['Name'])
              if ((common_words_dist<0.40 and dist>best_dist[0]) or (common_words_dist>0.40 and dist < best_dist[0])):
                best_dist = [dist,row['ID']]  
                
            # best_product = data[data['ID']==best_dist[1]]
            # best_product_desc = strToList(best_product['Description'].values[0])
            # print(best_product['Name'])
            # print("infer vec dist: ", descDist(best_product_desc,product_desc))
            # print("avg vect dist: ", nameDist(best_product_desc,product_desc))
                          
            if (best_dist[0]<0.85):  
              complementary.append(best_dist[1])
      print("T4: ", time.clock()-T0)
      product_cat_list = product_cat_list2
      complementary_cat = complementary_cat2
          
    res = [[],[]]
    for i in range(len(similar_above_mean)):
        res[0].append({'ID': similar_above_mean[i]})
    for i in range(len(complementary)):
        res[1].append({'ID': complementary[i]})
    return res
    
    


#set FLASK_APP=recommendations_api.py
#flask run

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SECRET_KEY'] = 'secret_key'

@app.route("/")
def test1():
    return 'test'

@app.route("/<id>", methods = ['POST'])
def test(id):
    if (request.method == 'POST'):
        return jsonify(findRecommendations(id))
        
if __name__ == '__main__':
    
    app.run(host=None,port=5000)