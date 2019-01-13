import os
import sys
import pickle
import json 

path = "C:\\Users\\quit7\\Desktop\\MOPSI\\code"
os.chdir(path)


def createTree():
    """
    Create a JSON tree with categories
    """ 
    cat1 = pickle.load(open('.\\data\\category1', 'rb'))
    cat2 = pickle.load(open('.\\data\\category2', 'rb'))
    cat3 = pickle.load(open('.\\data\\category3', 'rb'))
    tree = {}
    tree['module'] = 'Categories'
    children0 = []
    for c1 in range(len(cat1)):
        node1 = {}
        node1['module'] = cat1[c1]
        node1['path'] = cat1[c1]
        if (len(cat2[c1])==0):
            node1['leaf'] = True
        else:
            node1['collapsed'] = True
            children1 = []
            for c2 in range(len(cat2[c1])):
                node2 = {}
                node2['module'] = cat2[c1][c2]
                node2['path'] = cat1[c1]+', '+cat2[c1][c2]
                if (len(cat3[c1][c2])==0):
                    node1['leaf'] = True
                else:
                    node2['collapsed'] = True
                    children2 = []
                    for c3 in range(len(cat3[c1][c2])):
                        node3 = {}
                        node3['module'] = cat3[c1][c2][c3]
                        node3['path'] = cat1[c1]+', '+cat2[c1][c2]+', '+cat3[c1][c2][c3]
                        node3['leaf'] = True                   
                        children2.append(node3)
                    node2['children'] = children2
                children1.append(node2)
            node1['children'] = children1
        children0.append(node1)
    tree['children'] = children0
    with open('product_tree.json', 'wb') as fp:
        fp.write(json.dumps(tree).encode("utf-8"))
            
        
        
            
