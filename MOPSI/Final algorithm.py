import pandas
import os

##Import the data

path=r"C:\Users\Wissam\Desktop\IMI\MOPSI"
os.chdir(path)
import similarity_test
data = pandas.read_csv(r"enpc_raw_data_products_ng.csv",engine='python')
id=data.values[:,0]
product_names=data.values[:,1]
product_descriptions=data.values[:,2]
dsc_image_urls=data.values[:,3]
data2 = pandas.read_csv("data2_processed.csv")
d2v_model = doc2vec.Doc2Vec.load("d2v_model")

##Recategorize some misclassified products

categories=data.values[:,4]
categories[35396]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'
categories[372836]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'
categories[391207]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'

##Functions

def descriptionDistance(index1,index2,data2):
    desc1 = data2.loc[index1,'Description']
    desc2 = data2.loc[index2,'Description']
    vect1 = d2v_model.infer_vector(desc1)
    vect2 = d2v_model.infer_vector(desc2)
    return abs(spatial.distance.cosine(vect1, vect2))

def newindex(i):
  for k in range(len(data2)):
    if id[i]==data2.loc[k,'ID']:
      return k
      
def recommandations(product):
  c=[categories[product]]
  for i in range(len(product_names)):
    if categories[product].split(',')[0:-1]==categories[i].split(',')[0:-1] and categories[i] not in c:
      c.append(categories[i])
  rec=[]
  distances=[]
  for i in range(len(product_names)):
    if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and c[0] in categories[i]:
      d=1-similarity_test.evaluateSimilarity(product,i,data)
      d+=descriptionDistance(newindex(product),newindex(i),data2)
      distances.append((d,i))
  distances=sorted(distances)
  seuil=distances[3*len(distances)//4][0]
  rec.append(id[distances[0][1]]+' '+id[distances[1][1]]+' '+id[distances[2][1]]+' '+id[distances[3][1]]+' '+id[distances[4][1]])
  rec.append('')
  for k in range(1,len(c)):
    distances=[]
    for i in range(len(product_names)):
      if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and c[k] in categories[i]:
        d=1-similarity_test.evaluateSimilarity(product,i,data)
        d+=descriptionDistance(newindex(product),newindex(i),data2)
        if d>seuil:
          distances.append((d,i))
    distances=sorted(distances)
    for j in range(min(len(distances),3)):
      rec[-1]+=' '+id[distances[j][1]]
  rec[-1]=rec[-1][1:]
  return rec
  
##Main

with open(path1+r'ps4.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', escapechar=' ', quoting=csv.QUOTE_NONE)
    for i in range(len(product_names)):
      if categories[i]=='Root Category, Gaming, Playstation, PlayStation 4, Consoles' and str(product_descriptions[i])!='nan':
        rec=recommandations(i)
        if len(rec[1].split(' '))==6:
          print(i)
          r.writerow([id[i]]+rec)
