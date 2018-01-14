import os
from os import listdir
from os.path import isfile, join
import re
import string
import collections
import math
import csv
import pickle
import json
import parse_data as pd


#calculate tf_idf vector of each job posting
#input: list (a list that store information of each job postings that related to the job)
#output: none
def calculate_tf_idf(job_data, type_name):
	fread = open("../dictionary.txt", "r")
	str_text = fread.read()
	fread.close()
	temp_list = str_text.split("\n")[1:]

	word_dict = {}
	for i in range(0, len(temp_list)):
		index = temp_list[i].split("\t")[0]
		word = temp_list[i].split("\t")[1]
		df = temp_list[i].split("\t")[2]
		word_dict.update( { word:[index, df] } )

	tf_idf_list = []
	for i in range(0, len(job_data)):

		print ("iteration " + str(i))
		word_tf_idf = []
		for word, index_df in word_dict.items():
			tf = job_data[i]["all"].count(word)
			idf = math.log10(len(job_data)/int(index_df[1]))
			tf_idf = tf*idf
			# print ("tf: "+str(tf))
			# print ("df: "+str(df))
			# print ("idf: "+str(idf))
			if tf != 0:
				word_tf_idf.append( [index_df[0], tf_idf] )

		normalize = 0
		for i in range(0, len(word_tf_idf)):
			normalize += word_tf_idf[i][1]*word_tf_idf[i][1]
		normalize = math.sqrt(normalize)

		for i in range(0, len(word_tf_idf)):
			word_tf_idf[i][1] = word_tf_idf[i][1]/normalize
		tf_idf_list.append(word_tf_idf)

	print (tf_idf_list)

	if type_name == "generate":
		filename = "../tf_idf.p"
		fread = open(filename, "wb")
		pickle.dump(tf_idf_list, fread)
		fread.close()
	else:
		return (tf_idf_list)

# job_data = pd.parse_data()
# calculate_tf_idf(job_data, "generate")
