#------- Import self-defined function files -------#
import numpy as np
import json
import pickle
import sys
# sys.path.append('./function')
import tf_idf as tf_idf
import cosine_similarity as cs
import cluster as cluster

#------- Functions -------#
def compute_cosine_similarity(input_tf_idf_array):

    print("Start compute_cosine_similarity")
    new_fileObject = open("../tf_idf.p",'rb')
    tf_idf = pickle.load(new_fileObject)
    # with open('./tf_idf.txt') as json_file:
    #     tf_idf = json.load(json_file)
    doc_num = len(tf_idf)

    temp_input_cs = [0 for x in range(doc_num)]
    for i in range(0,len(tf_idf)):
        temp_input_cs[i] = cs.cosine(tf_idf[i],input_tf_idf_array[0])
    max_cluster = get_cluster(temp_input_cs)
    return max_cluster

def get_cluster(temp_input_cs):
    print("Start cluster")
    new_fileObject = open("../clusters_20.p",'rb')
    clusters = pickle.load(new_fileObject)

    temp_input_cs_arr = np.array(temp_input_cs)
    max_doc = temp_input_cs_arr.argsort()[-3:][::-1]
    temp_input_cs.sort(reverse=True)
    max_value = [temp_input_cs[0],temp_input_cs[1],temp_input_cs[2]]
    max_cluster = [clusters[max_doc[0]],clusters[max_doc[1]],clusters[max_doc[2]]]
    return [max_doc,max_value,max_cluster]

#------- Main Functions -------#
file_name = sys.argv[1]
# input_document = sys.argv[2]
fread = open("../test_document/"+file_name, "r")
input_document = fread.read()
input_document.replace("\n", " ")
input_document.replace("\n\n", " ")
fread.close()

input_data_dict = {}
input_data_dict[0] = {}
input_data_dict[0]["all"] = input_document

input_tf_idf_array = tf_idf.calculate_tf_idf(input_data_dict,"INPUT")
result = compute_cosine_similarity(input_tf_idf_array)
print(result)
