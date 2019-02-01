from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import pandas as pd

path = "C:\\Users\\quit7\\Desktop\\MOPSI\\code"
os.chdir(path)

def strToList(x):
    """
    Transform "['a', 'b']" into ['a', 'b']
    """
    if type(x)==str:
        return x[2:-2].split("', '")

data = pd.read_csv(".\\data\\data2_processed.csv")
data = data.drop(['SmallImage'], axis=1)
data.Name = data.Name.apply(strToList)
data.Description = data.Description.apply(strToList)
#data.Categories = data.Categories.apply(strToList)


def findRecommendations(id):
    product_cat_str = data[data['ID']==id]['Categories'].values[0]
    #product_cat_str = data[data['ID']=='WA442EL0A105ZNAFAMZ']['Categories'].values[0]
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