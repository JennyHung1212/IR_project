#------- Import self-defined function files -------#
import numpy as np
import json
import sys
sys.path.append('./function')
import tf_idf as tf_idf
import cosine_similarity as cs
import cluster as cluster

#------- Functions -------#
def compute_cosine_similarity(input_tf_idf_array):

    # new_fileObject = open("./tf_idf.p",'rb')
    # tf_idf = pickle.load(new_fileObject)
    with open('./tf_idf.txt') as json_file:
        tf_idf = json.load(json_file)

    temp_input_cs = []
    for i in range(0,len(tf_idf)):
        temp_input_cs[i] = cs.cosine(tf_idf[i],input_tf_idf_array[0])
    max_cluster = get_cluster(temp_input_cs)
    return max_cluster

def get_cluster(temp_input_cs):
    with open('./clusters_8.txt') as temp_json_file:
        clusters = json.load(temp_json_file)
    max_doc = temp_input_cs.argsort()[-3:][::-1]
    max_cluster = [clusters[max_doc[0]],clusters[max_doc[1]],clusters[max_doc[2]]]
    return [max_doc,max_cluster]

#------- Main Functions -------#
file_name = sys.argv[1]
input_document = sys.argv[2]
input_tf_idf_array = tf_idf.calculate_tf_idf([input_document],"INPUT")

result = compute_cosine_similarity(input_tf_idf_array)
print(result)
