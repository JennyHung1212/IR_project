import pickle
import json

fread = open("../tf_idf.json", "r")
tf_idf_list = json.load(fread)
fread.close()

fread = open("../tf_idf.p", "wb")
pickle.dump(tf_idf_list, fread)
fread.close
