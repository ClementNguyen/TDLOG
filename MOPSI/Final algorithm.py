import pandas

##Import the data

path=r"C:\Users\Wissam\Desktop\IMI\MOPSI\\"
data = pandas.read_csv(path+r"enpc_raw_data_products_ng.csv",engine='python')
id=data.values[:,0]
product_names=data.values[:,1]
product_descriptions=data.values[:,2]
dsc_image_urls=data.values[:,3]

##Recategorize some misclassified products

categories=data.values[:,4]
categories[35396]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'
categories[372836]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'
categories[391207]='Root Category, Gaming, Playstation, PlayStation 4, Consoles'

