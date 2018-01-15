import numpy as np
import json
import pickle
import string
import collections

fread = open("../dictionary.txt", "r")
str_text = fread.read()
fread.close()
temp_list = str_text.split("\n")[1:]

word_dict = {}
for i in range(0, len(temp_list)):
    index = temp_list[i].split("\t")[0]
    word = temp_list[i].split("\t")[1]
    df = temp_list[i].split("\t")[2]
    word_dict.update( { index:word } )

new_fileObject = open("../tf_idf.p",'rb')
tf_idf = pickle.load(new_fileObject)
doc_num = len(tf_idf)

for i in range(0,doc_num):
    temp_index = 0
    word_index_array = [0 for x in range(len(tf_idf[i]))]
    tf_idf_array = [0 for x in range(len(tf_idf[i]))]
    for each_tf_idf in tf_idf[i]:
        # word_index
        word_index_array[temp_index] = each_tf_idf[0]
        # tf-idf
        tf_idf_array[temp_index] = each_tf_idf[1]
        temp_index += 1

    temp_input_tf_idf_arr = np.array(tf_idf_array)
    if i == 508 or i == 1569 or i == 2948 or i == 3628 or i == 3629:
        max_tf_idf = temp_input_tf_idf_arr.argsort()[-1:][::-1]
        max_index = [word_index_array[max_tf_idf[0]]]
        max_word = [word_dict[max_index[0]]]
        print("doc: ",i)
        print("tf_idf: ",[tf_idf_array[max_tf_idf[0]]])
        print("word: ",max_word)
    else:
        max_tf_idf = temp_input_tf_idf_arr.argsort()[-3:][::-1]
        max_index = [word_index_array[max_tf_idf[0]],word_index_array[max_tf_idf[1]],word_index_array[max_tf_idf[2]]]
        max_word = [word_dict[max_index[0]],word_dict[max_index[1]],word_dict[max_index[2]]]
        print("doc: ",i)
        print("tf_idf: ",[tf_idf_array[max_tf_idf[0]],tf_idf_array[max_tf_idf[1]],tf_idf_array[max_tf_idf[2]]])
        print("word: ",max_word)
