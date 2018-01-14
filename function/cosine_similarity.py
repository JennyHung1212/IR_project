import collections
from collections import Counter
import os
import os.path
import glob
import math
import nltk
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist
from nltk.tokenize import RegexpTokenizer
import pickle
import json

def cosine(doc_x, doc_y, func_type):

    # read input
    # fileObject = open("../tf_idf.p",'rb')
    # data = pickle.load(fileObject)
    with open('../tf_idf.txt') as json_file:
        tf_idf = json.load(json_file)

    if(func_type == "CLUSTER"):
        #doc_ti_vector_x = data[int(doc_x)]
        #doc_ti_vector_y = data[int(doc_y)]
        doc_ti_vector_x = data[0]
        doc_ti_vector_y = data[0]
        #doc_ti_vector_x = doc_ti_vector_x_data.items()
        #doc_ti_vector_y = doc_ti_vector_y_data.items()
    elif(func_type == "INPUT"):
        doc_ti_vector_x = doc_x
        doc_ti_vector_y = doc_y

    doc_x_p = 0
    doc_y_p = 0
    cosine = 0

    while doc_x_p < len(doc_ti_vector_x) and doc_y_p < len(doc_ti_vector_y):
        doc_x_id = int(doc_ti_vector_x[doc_x_p][0])
        doc_y_id = int(doc_ti_vector_y[doc_y_p][0])
        doc_x_ti_vec = float(doc_ti_vector_x[doc_x_p][2])
        doc_y_ti_vec = float(doc_ti_vector_y[doc_y_p][2])

        if doc_x_id == doc_y_id:
            cosine += doc_x_ti_vec * doc_y_ti_vec
            doc_x_p += 1
            doc_y_p += 1
        elif doc_x_id < doc_y_id:
            doc_x_p += 1
        elif doc_x_id > doc_y_id:
            doc_y_p += 1

    return cosine

# def doc_ti_vector(doc):
#     # read input
#     fileObject = open("../tf_idf.p",'rb')
#     data = pickle.load(fileObject)

#     data_split = []
#     for text in data.split("\n"):
#         data_split.append(text.split("\t"))
#     data_split.pop(len(data_split)-1)

#     return data_split

print(cosine("1","2"))
