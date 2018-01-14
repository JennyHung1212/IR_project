import os
from os import listdir
from os.path import isfile, join
import string
import collections
import math
import pickle
import json
import sys
sys.path.append('./function')
import tf_idf as tf_idf
import cosine_similarity as cs

def do_HAC():

    new_fileObject = open("../tf_idf.p",'rb')
    tf_idf = pickle.load(new_fileObject)
    # with open('../tf_idf.txt') as json_file:
    #     tf_idf = json.load(json_file)

    doc_num = len(tf_idf)
    print ("doc_num: " +str(doc_num))
    C = [[0 for x in range(doc_num)] for y in range(doc_num)]
    I = [1 for x in range(doc_num)]
    A = []
    cluster_dis = [[y] for y in range(1,doc_num+1)]
    cluster_num = doc_num

    # Initialize
    print("Initialize")
    # for n in range(0,doc_num):
    #     print(n)
    #     for i in range(n+1,doc_num):
    #         C[n][i] = cs.cosine(tf_idf[n],tf_idf[i])
    #     I[n] = 1
    #
    # #pkl file
    # fileObject = open("../cs_table.p",'wb')
    # pickle.dump(C,fileObject)
    # fileObject.close()

    new_fileObject = open("../cs_table.p",'rb')
    C = pickle.load(new_fileObject)

    print("Calculate")
    for k in range(0,doc_num-1):
        print(k)
        merge_index = [0,0]
        merge_index = find_argmax(C, doc_num, I)
        A.append(merge_index)
        # print(cluster_dis[merge_index[1]])
        cluster_dis[merge_index[0]].extend(cluster_dis[merge_index[1]])
        cluster_dis[merge_index[1]] = 0

        # print(cluster_dis[merge_index[0]])
        for j in range(0,doc_num):
            max_sim = min(C[j][merge_index[0]],C[j][merge_index[1]])
            C[merge_index[0]][j] = max_sim
            C[j][merge_index[0]] = max_sim
        I[merge_index[1]] = 0
        cluster_num -= 1

        if cluster_num == 8 or cluster_num == 13 or cluster_num == 20:
            print_txt_file(cluster_num,cluster_dis)
            convert_json(cluster_num,cluster_dis,doc_num)


def find_argmax(C, doc_num, I):
    max_value = 0
    merge_index = [0,0]
    for n in range(0,doc_num):
        for i in range(n+1,doc_num):
            if I[n] and I[i]:
                if C[n][i] >= max_value:
                    max_value = C[n][i]
                    if n > i:
                        merge_index[0] = i
                        merge_index[1] = n
                    else:
                        merge_index[0] = n
                        merge_index[1] = i
    return merge_index

def print_txt_file(cluster_num,cluster_dis):
    temp_file_name = str(cluster_num)+".txt"
    fwrite = open("../"+temp_file_name ,"w")
    for cluster_array in cluster_dis:
        if cluster_array != 0:
            temp_sort_array = sorted(cluster_array)
            for value in temp_sort_array:
                fwrite.write(str(value)+"\n")
            fwrite.write("\n")

def convert_json(cluster_num,cluster_dis,doc_num):
    cluster_data = [0 for x in range(doc_num)]
    cluster_count = 0
    for cluster_array in cluster_dis:
        if cluster_array != 0:
            for doc in cluster_array:
                cluster_data[doc-1] = cluster_count
            cluster_count += 1

    #pkl file
    temp_file_name = "clusters_"+str(cluster_num)+".p"
    fileObject = open("../"+temp_file_name,'wb')
    pickle.dump(cluster_data,fileObject)
    fileObject.close()

# do_HAC()
