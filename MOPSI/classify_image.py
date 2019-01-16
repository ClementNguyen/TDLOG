from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pandas
from PIL import Image
import requests
from io import BytesIO
import argparse
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import sys
import tarfile
import numpy as np
from six.moves import urllib
os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
import tensorflow as tf
import csv
import urllib.request
from urllib.request import Request, urlopen
import requests
import shutil
import re, math
from collections import Counter
from scipy import spatial
import gensim

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

path=r"C:\Users\Wissam\Desktop\IMI\\"
path1=path+r"MOPSI\\" #folder containing the .csv file
path2=path1+r"Images\\" #folder that will store the images
data = pandas.read_csv(path1+r"enpc_raw_data_products_ng.csv",engine='python')
id=data.values[:,0]
product_names=data.values[:,1]
product_descriptions=data.values[:,2]
dsc_image_urls=data.values[:,3]
categories=data.values[:,4]
model = gensim.models.KeyedVectors.load_word2vec_format(path1+'GoogleNews-vectors-negative300.bin', binary=True)  
index2word_set = set(model.wv.index2word)
coeffw=1 #weight of Wissam's method
coeffc=2 #weight of Clément's method
#similaritylimit=0.7

os.chdir(r"C:\Users\Wissam\Desktop\IMI\MOPSI\models-master\tutorials\image\imagenet")
import similarity_test

def isnull(list):
  for i in range(len(list)):
    if list[i]!=0:
      return False
  return True

def levenshtein(seq1, seq2):  
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])


def avg_feature_vector(sentence, model, num_features, index2word_set):
    sentence=sentence.replace(',', '')
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec
    
def sentence_distance(text1,text2):
    s1=avg_feature_vector(text1, model=model, num_features=300, index2word_set=index2word_set)
    s2=avg_feature_vector(text2, model=model, num_features=300, index2word_set=index2word_set)
    return spatial.distance.cosine(s1, s2)
    
def product_distance(product1,product2):
  img_url1=str(dsc_image_urls[product1])
  img_url2=str(dsc_image_urls[product2])
  img_filename1=product_names[product1].replace('"','').replace("/","").replace("\\","").replace(":","").replace("*","").replace("?","").replace("<","").replace(">","").replace("|","")
  img_filename2=product_names[product2].replace('"','').replace("/","").replace("\\","").replace(":","").replace("*","").replace("?","").replace("<","").replace(">","").replace("|","")
  r1 = requests.get(img_url1, stream=True)
  if r1.status_code == 200:
    with open(path2+img_filename1, 'wb') as f:
        r1.raw.decode_content = True
        shutil.copyfileobj(r1.raw, f)
  r2 = requests.get(img_url2, stream=True)
  if r2.status_code == 200:
    with open(path2+img_filename2, 'wb') as f:
        r2.raw.decode_content = True
        shutil.copyfileobj(r2.raw, f)
  image1 = (FLAGS.image_file if FLAGS.image_file else
            os.path.join(FLAGS.model_dir, path2+img_filename1))
  image2 = (FLAGS.image_file if FLAGS.image_file else
            os.path.join(FLAGS.model_dir, path2+img_filename2))
  labels_and_scores1=run_inference_on_image(image1) 
  labels_and_scores2=run_inference_on_image(image2)
  distance=0
  for i in range(len(labels_and_scores1)):
    for j in range(len(labels_and_scores2)):
      distance+=labels_and_scores1[i][1]*labels_and_scores2[j][1]*sentence_distance(labels_and_scores1[i][0],labels_and_scores2[j][0])
  return distance

FLAGS = None

# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# pylint: enable=line-too-long

class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.
    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.
    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(image):
  """Runs inference on an image.
  Args:
    image: Image file name.
  Returns:
    Nothing
  """
  if not tf.gfile.Exists(image):
    tf.logging.fatal('File does not exist %s', image)
  image_data = tf.gfile.FastGFile(image, 'rb').read()

  # Creates graph from saved GraphDef.
  create_graph()

  with tf.Session() as sess:
    # Some useful tensors:
    # 'softmax:0': A tensor containing the normalized prediction across
    #   1000 labels.
    # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
    #   float description of the image.
    # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
    #   encoding of the image.
    # Runs the softmax tensor by feeding the image_data as input to the graph.
    softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
    predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
    predictions = np.squeeze(predictions)

    # Creates node ID --> English string lookup.
    node_lookup = NodeLookup()
    
    labels_and_scores=[]

    top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
    for node_id in top_k:
      human_string = node_lookup.id_to_string(node_id)
      score = predictions[node_id]
      list = human_string.split(',')
      words=[]
      for word in list:
        if not isnull(avg_feature_vector(word, model=model, num_features=300, index2word_set=index2word_set)):
          words.append(word)
      if len(words)>0:
        human_string=words[0]
        for i in range(1,len(words)):
          human_string+=', '+words[i]
        labels_and_scores.append([human_string,score])
  return labels_and_scores
    


def maybe_download_and_extract():
  """Download and extract model tar file."""
  dest_directory = FLAGS.model_dir
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    def _progress(count, block_size, total_size):
      sys.stdout.write('\r>> Downloading %s %.1f%%' % (
          filename, float(count * block_size) / float(total_size) * 100.0))
      sys.stdout.flush()
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
    print()
    statinfo = os.stat(filepath)
    print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
  tarfile.open(filepath, 'r:gz').extractall(dest_directory)
  
def recommandations(product):
  c=[categories[product].split(',')[-1]] #list of categories in which we will search
  for i in range(len(product_names)):
    if categories[product].split(',')[0:-1]==categories[i].split(',')[0:-1] and categories[i].split(',')[-1] not in c:
      c.append(categories[i].split(',')[-1])
  list=[]
  for category in c:
    distances=[]
    for i in range(len(product_names)):
      if product_names[i]!=product_names[product] and str(product_descriptions[i])!='nan' and str(dsc_image_urls[i])!='nan' and categories[product].split(',')[0:-1]==categories[i].split(',')[0:-1] and categories[i].split(',')[-1]==category:
        distances.append((coeffc*(1-similarity_test.evaluateSimilarity(product,i,data),i)))
    distances=sorted(distances)
    list.append(id[distances[0][1]])
  return list


def main():
  # maybe_download_and_extract()
  
  with open(path1+r'recommandations.csv', mode='w', newline="") as csvfile:
    r = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(product_names)):
      if categories[i]=='Root Category, Phones & Tablets, Accessories, Cases, Mobile Phones':
        print(i)
        r.writerow([id[i]]+recommandations(i))
  
  
  # product1=3
  # product2=14
  # if str(dsc_image_urls[product1])=='nan':
  #   print('The product ',product1, ' has no image.')
  # if str(dsc_image_urls[product2])=='nan':
  #   print('The product ',product2, ' has no image.')
  # else:
  #   dw=product_distance(product1,product2)
  #   print('The distance between ',product_names[product1], ' and ',product_names[product2],' is : ',dw, ', according to Wissam\'s algorithm')
  #   dc=1-similarity_test.evaluateSimilarity(product1,product2,data)
  #   print('The distance between ',product_names[product1], ' and ',product_names[product2],' is : ',dc, ', according to Clément\'s algorithm')
  #   d=coeffw*dw+coeffc*dc
  #   print('The total distance between ',product_names[product1], ' and ',product_names[product2],' is : ',d)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  # classify_image_graph_def.pb:
  #   Binary representation of the GraphDef protocol buffer.
  # imagenet_synset_to_human_label_map.txt:
  #   Map from synset ID to a human readable string.
  # imagenet_2012_challenge_label_map_proto.pbtxt:
  #   Text representation of a protocol buffer mapping a label to synset ID.
  parser.add_argument(
      '--model_dir',
      type=str,
      default='/tmp/imagenet',
      help="""\
      Path to classify_image_graph_def.pb,
      imagenet_synset_to_human_label_map.txt, and
      imagenet_2012_challenge_label_map_proto.pbtxt.\
      """
  )
  parser.add_argument(
      '--image_file',
      type=str,
      default='',
      help='Absolute path to image file.'
  )
  parser.add_argument(
      '--num_top_predictions',
      type=int,
      default=5,
      help='Display this many predictions.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  main()
