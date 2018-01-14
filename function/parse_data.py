import os
from os import listdir
from os.path import isfile, join
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import collections
import math
import csv
import pickle

# parse from data_job_posts_xs.csv and output a structured dictionary
#   input: none
#   output: dictionary
def parse_data():
    print("Start load file")
    # Read File
    fread = open("../dataset/data_job_posts_only_doc.csv" ,"r")
    csvCursor = csv.reader(fread)

    row_count = -1
    data_key = []
    data_dict = {}
    all_data_dict = {}
    row_index = 0
    for row in csvCursor:
        # if row_count == -1:
            # for i in range(0,5):
            #     data_key[i] = row[i]
            # # date
            # data_key[0] = row[0]
            # # title
            # data_key[1] = row[1]
            # # job description
            # data_key[2] = row[2]
            # # job requirement
            # data_key[3] = row[3]
            # # required quality
            # data_key[4] = row[4]
        # else:
        if row_count >= 15242:
            all_data_dict[row_index] = {}
            all_data_dict[row_index]["all"] = row[1]
            if row[2] != "NA":
                all_data_dict[row_index]["all"] += " " + row[2]
            if row[3] != "NA":
                all_data_dict[row_index]["all"] += " " + row[3]
            if row[4] != "NA":
                all_data_dict[row_index]["all"] += " " + row[4]
            row_index += 1
            # for j in range(0,5):
            #     data_dict[row_count][data_key[j]] = row[j]
        row_count += 1

    fread.close()
    return all_data_dict

# Record the document frequency of each term and save it as a txt file (dictionary.txt)
def construct_dictionary(data_dict):
    print("Start construct dictionary")
    term_array = []
    for i in range(0,len(data_dict)):
        term_array_set = set(collect_text(data_dict, i, "all"))
        term_array += term_array_set
    term_array.sort()
    record_df(term_array)

# Tokenize the given file and also do stemming, stopwords removal and return the term list
#   input:document id and what to collect
#   output:the term list
def collect_text(data_dict, post, column_title):

    # Get content
    # content = parse_data()
    content = data_dict[post][column_title]
    content.replace("\n\n", " ")
    content.replace("\n", " ")
    content = content.lower()

    # Tokenization
    tokenizer = RegexpTokenizer(r'\w+')
    content = tokenizer.tokenize(content)

    # Stemming and Lemmatization
    ps = PorterStemmer()
    content = [ps.stem(word) for word in content]

    # Stop words
    stoplist = set(stopwords.words('english'))
    content = [word for word in content if (word not in stoplist and word.find("_") == -1 and len(word)>3) and not any(char.isdigit() for char in word)]
    return content

# Record the document frequency of each term
#   input:term_array, which is a list with each document's terms
def record_df(term_array):
    sorted_term_frequency = get_term_frequency_array(term_array)
    print_out_df(sorted_term_frequency)

# Get each term's frequency and sort them
#   input:term_array, which is a list with each document's terms
#   output:sorted_term_frequency, sorted_term_frequency[word]=df of such word
def get_term_frequency_array(term_array):
    term_frequency = {}
    for word in term_array:
        count = term_frequency.get(word,0)
        term_frequency[word] = count + 1
    sorted_term_frequency = collections.OrderedDict(sorted(term_frequency.items()))
    return(sorted_term_frequency)

# Print out the txt file and the pkl file
def print_out_df(sorted_term_frequency):
    print("Start print out df")

    #txt file
    index_counter = 1
    result_content = "t_index\tterm\tdf"
    for word in sorted_term_frequency:
        result_content += "\n"+str(index_counter)+"\t"+word+"\t"+str(sorted_term_frequency[word])
        index_counter += 1
    fwrite = open("../dictionary.txt" ,"w")
    fwrite.write(result_content)

    #pkl file
    fileObject = open("../dictionary.p",'wb')
    pickle.dump(sorted_term_frequency,fileObject)
    fileObject.close()


# data_dict = parse_data()
# construct_dictionary(data_dict)
