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

# parse from data_job_posts_xs.csv and output a structured dictionary
#   input: none
#   output: dictionary
def parse_data():

    # Read File
    fread = open("../dataset/data_job_posts_xs.csv" ,"r")
    csvCursor = csv.reader(fread)

    row_count = -1
    data_key = []
    data_dict = {}
    for row in csvCursor:
        if row_count == -1:
            for i in range(0,5):
                # date
                data_key[i] = row[i]
            # title
            # data_key[1] = row[1]
            # job description
            # data_key[2] = row[2]
            # job requirement
            # data_key[3] = row[3]
            # required quality
            # data_key[4] = row[4]
        else:
            for j in range(0,5):
                data_dict[row_count][data_key[j]] = row[j]
        row_count += 1
    fread.close()
    return data_dict

# Tokenize the given file and also do stemming, stopwords removal and return the term list
#   input:document id and what to collect
#   output:the term list
def collect_text(data_dict, post, column_title):

    # Get content
    # content = parse_data()
    content = data_dict[post][column_title]

    # Tokenization
    tokenizer = RegexpTokenizer(r'\w+')
    content = tokenizer.tokenize(content)

    # Stemming and Lemmatization
    ps = PorterStemmer()
    content = [ps.stem(word) for word in content]

    # Stop words
    stoplist = set(stopwords.words('english'))
    content = [word for word in content if (word not in stoplist and word.find("_") == -1) and not any(char.isdigit() for char in word)]
    return content

# Record the document frequency of each term
#   input:term_array, which is a list with each document's terms
def record_df(term_array):
    sorted_term_frequency = get_term_frequency_array(term_array)
    index_counter = 1
    for word in sorted_term_frequency:
        result_content += "\n"+str(index_counter)+"\t"+word+"\t"+str(sorted_term_frequency[word])
        index_counter += 1
    fwrite = open("../dictionary.txt" ,"w")
    fwrite.write(result_content)

# Get each term's frequency and sort them
#   input:term_array, which is a list with each document's terms
def get_term_frequency_array(term_array):
    term_frequency = {}
    for word in term_array:
        count = term_frequency.get(word,0)
        term_frequency[word] = count + 1
    sorted_term_frequency = collections.OrderedDict(sorted(term_frequency.items()))
    return(sorted_term_frequency)

data_dict = parse_data()
term_array = []
for i in len(data_dict):
    temp_term = set(collect_text(data_dict, i, "JobDescription"))
    term_array += temp_term
record_df(term_array)
