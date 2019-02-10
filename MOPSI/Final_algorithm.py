import pandas
import os
from gensim.models import doc2vec
import csv
import requests
import random

##Import the data

path=r"C:\Users\wissa\OneDrive\Bureau\MOPSI"
os.chdir(path)
data = pandas.read_csv(r"enpc_raw_data_products_ng.csv",engine='python')
id=data.values[:,0]
product_names=data.values[:,1]
product_descriptions=data.values[:,2]
dsc_image_urls=data.values[:,3]
categories=data.values[:,4]
import similarity_test
import yolo
os.chdir(path)

##Functions

def laptop_recommandations(product):
  c=[categories[product].split(',')[0:4]]
  for i in range(len(product_names)):
    if categories[product].split(',')[0:3]==categories[i].split(',')[0:3] and categories[i].split(',')[0:4] not in c:
      c.append(categories[i].split(',')[0:4])
  del c[4]
  del c[4]
  del c[4]
  del c[-1]
  rec=[]
  distances=[]
  for i in range(len(product_names)):
    if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and categories[i].split(',')[0:4]==c[0]:
      d=1-similarity_test.evaluateSimilarity(product,i,data)
      distances.append((d,i))
  distances=sorted(distances)
  rec=[id[distances[0][1]]]
  titles=[product_names[distances[0][1]]]
  n=5 #number of similar products
  i=1
  while len(titles)<n:
    if product_names[distances[i][1]] not in titles:
      titles.append(product_names[distances[i][1]])
      rec[0]+=' '+id[distances[i][1]]
    i+=1
  rec.append('')
  for k in range(1,len(c)):
    distances=[]
    for i in range(len(product_names)):
      if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and categories[i].split(',')[0:4]==c[k]:
        d=1-similarity_test.evaluateSimilarity(product,i,data)
        distances.append((d,i))
    distances=sorted(distances)
    admissibles=[]
    j=0
    for l in range(5):
      img = requests.get(dsc_image_urls[distances[j][1]]).content
      name='product.jpg'
      with open(yolo.image_path+name, 'wb') as handler:
        handler.write(img)
      y=yolo.detect(name)
      while product_names[distances[j][1]] in titles or y==['laptop'] or 'tvmonitor' in y:
        j+=1
        img = requests.get(dsc_image_urls[distances[j][1]]).content
        name='product.jpg'
        with open(yolo.image_path+name, 'wb') as handler:
          handler.write(img)
        y=yolo.detect(name)
      admissibles.append(distances[j][1])
      j+=1
    i1,i2=random.sample(admissibles,2)
    rec[-1]+=' '+id[i1]+' '+id[i2]
    titles.append(product_names[i1])
    titles.append(product_names[i2])
  rec[-1]=rec[-1][1:]
  return rec

def ps4_recommandations(product):
  c=[categories[product]]
  for i in range(len(product_names)):
    if categories[product].split(',')[0:-1]==categories[i].split(',')[0:-1] and categories[i] not in c:
      c.append(categories[i])
  distances=[]
  for i in range(len(product_names)):
    if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and c[0] in categories[i]:
      d=1-similarity_test.evaluateSimilarity(product,i,data)
      distances.append((d,i))
  distances=sorted(distances)
  seuil=distances[3*len(distances)//4][0]
  rec=[id[distances[0][1]]]
  titles=[product_names[distances[0][1]]]
  n=5 #number of similar products
  i=1
  while len(titles)<n:
    if product_names[distances[i][1]] not in titles:
      titles.append(product_names[distances[i][1]])
      rec[0]+=' '+id[distances[i][1]]
    i+=1
  rec.append('')
  for k in range(1,len(c)):
    distances=[]
    for i in range(len(product_names)):
      if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and c[k] in categories[i] and 'Playstation 2' not in product_names[i] and 'PS2' not in product_names[i] and 'PlayStation 2' not in product_names[i] and 'Ps2' not in product_names[i] and 'PS 2' not in product_names[i] and 'Ps 2' not in product_names[i]:
        d=1-similarity_test.evaluateSimilarity(product,i,data)
        if d>seuil:
          distances.append((d,i))
    distances=sorted(distances)
    if len(distances)>0:
      titles=[product_names[distances[0][1]]]
      rec[-1]+=' '+id[distances[0][1]]
    n=2 #number of complementary products
    j=1
    while len(titles)<n+1 and j<len(distances):
      if product_names[distances[j][1]] not in titles:
        titles.append(product_names[distances[j][1]])
        rec[-1]+=' '+id[distances[j][1]]
      j+=1
  rec[-1]=rec[-1][1:]
  return rec
  
##Main

with open(r'bikes.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE)
    for i in range(len(product_names)):
      if categories[i]=='Root Category, Sporting Goods, Outdoor Recreation, Cycling, Bikes' and str(dsc_image_urls[i])!='nan' and str(product_descriptions[i])!='nan':
        img = requests.get(dsc_image_urls[i]).content
        img_name=product_names[i].replace('"','').replace("/","").replace("\\","").replace(":","").replace("*","").replace("?","").replace("<","").replace(">","").replace("|","").replace(".","")+'.jpg'
        with open(yolo.image_path+img_name, 'wb') as handler:
          handler.write(img)
        if 'bicycle' in yolo.detect(img_name):
          rec=bike_recommandations(i,img_name)
          if len(rec[1].split(' '))==6:
            print(i)
            r.writerow([id[i]]+rec)


with open(r'ps4.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE)
    for i in range(len(product_names)):
      if categories[i]=='Root Category, Gaming, Playstation, PlayStation 4, Consoles' and str(dsc_image_urls[i])!='nan' and str(product_descriptions[i])!='nan':
        rec=ps4_recommandations(i)
        if len(rec[1].split(' '))==6:
          print(i)
          r.writerow([id[i]]+rec)  
          
          
with open(r'laptops_2.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE)
    for i in range(508,len(product_names)):
      if categories[i]=='Root Category, Computing, Computers & Accessories, Computers & Tablets, Laptops' and str(dsc_image_urls[i])!='nan' and str(product_descriptions[i])!='nan':
        img = requests.get(dsc_image_urls[i]).content
        img_name='laptop.jpg'
        with open(yolo.image_path+img_name, 'wb') as handler:
          handler.write(img)
        if ['laptop']==yolo.detect(img_name):
          rec=laptop_recommandations(i)
          if len(rec[1].split(' '))==8:
            r.writerow([id[i]]+rec)
            
with open(r'ventilateurs.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE)
    for i in range(len(product_names)):
      if categories[i]=='Root Category, Home & Office, Appliances, Home & Kitchen, Heating, Cooling & Air Quality, Household Fans, Pedestal Fans, Tools & Home Improvement, Appliances, Large Appliance Accessories' and str(dsc_image_urls[i])!='nan' and str(product_descriptions[i])!='nan':
        img = requests.get(dsc_image_urls[i]).content
        img_name='laptop.jpg'
        with open(yolo.image_path+img_name, 'wb') as handler:
          handler.write(img)
        if ['laptop']==yolo.detect(img_name):
          rec=laptop_recommandations(i)
          if len(rec[1].split(' '))==8:
            r.writerow([id[i]]+rec)
            
          
