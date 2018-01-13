import os
from os import listdir
from os.path import isfile, join
import re
import string
import collections
import math
import csv
import pickle

#parse csv to list
#input: none
#output: list (a list that store information of each job postings that related to the job)
def parse_data():
	job_data = []
	fread = open("../dataset/data_job_posts_xs.csv" ,"r")
	csvCursor = csv.reader(fread)

	for row in csvCursor:
		if row[0] != "date":
			job_info = ""
			#Title+JobDescription+JobRequirement+RequireQual
			if row[1] != "NA":
				job_info += row[1]
			if row[7] != "NA":
				job_info += row[7]
			if row[8] != "NA":
				job_info += row[8]
			if row[9] != "NA":
				job_info += row[9]
			job_data.append(job_info)  


	fread.close()
	return job_data


#calculate tf_idf vector of each job posting
#input: list (a list that store information of each job postings that related to the job)
#output: none
def calculate_tf_idf(job_data):
	fread = open("../dictionary.txt", "r")
	str_text = fread.read()
	fread.close()
	temp_list = str_text.split("\n")[:-1]

	word_dict = {}
	for i in range(0, len(temp_list)):
		word = temp_list[i].split("\t")[1]
		df = temp_list[i].split("\t")[2]
		word_dict.update( { word:df } )

	tf_idf_list = []
	for i in range(0, len(job_data)):
		word_tf_idf = {}
		print ("N: "+ str(len(job_data)))
		for word, df in word_dict.items():
			tf = job_data[i].count(word)
			idf = math.log10(len(job_data)/int(df))
			tf_idf = tf*idf
			print ("tf: "+str(tf))
			print ("df: "+str(df))
			print ("idf: "+str(idf))
			if tf != 0:
				word_tf_idf.update( {word:tf_idf} )

		normalize = 0
		for word, tf_idf in word_tf_idf.items():
			normalize += tf_idf*tf_idf
		normalize = math.sqrt(normalize)

		for word, tf_idf in word_tf_idf.items():
			word_tf_idf[word] = word_tf_idf[word]/normalize
			print (word_tf_idf[word])

		tf_idf_list.append(word_tf_idf)
		break
	
	fread = open("../tf_idf.p", "wb")
	pickle.dump(tf_idf_list, fread)
	fread.close()
		
N = 0
temp = parse_data()
calculate_tf_idf(temp)



