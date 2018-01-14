# feature_selection
def do_feature_selection(classification,document,k):
    llr_array = {}
    final_array = []
    term_set = get_term_set(classification,document)

    for t in term_set:
        llr_array[t] = get_llr_value(document,t,classification)

    sorted_keys = sorted(llr_array, key=llr_array.get, reverse=True)
    counter = 0
    for key in sorted_keys:
        if counter < k:
            final_array.append(key)
        counter += 1
    return final_array

def get_term_set(classification,document):
    term_array = []
    for c in classification:
        for doc in classification[c]:
            term_array_set = set(document[doc])
            term_array += term_array_set
    term_array = set(term_array)
    return term_array

def concatenate_text_set(document,classification_array):
    result_array = []
    for d in classification_array:
        temp_set = set(document[d])
        result_array += temp_set
    return result_array
def concatenate_other_text_set(document,classification,given_class):
    result_array = []
    for c in classification:
        if(c != given_class):
            for d in classification[c]:
                temp_set = set(document[d])
                result_array += temp_set
    return result_array

# likelihood ratio
def get_llr_value(document,t,classification):
    llr_value = []
    class_document = 15
    other_document = 13*15 - class_document

    for c in classification:
        temp_llr_value = 0
        stat = [[0,0],[0,0]]

        # new version, faster
        for llr_doc_class in classification:
            if llr_doc_class == c:
                for doc in classification[llr_doc_class]:
                    if t in document[doc]:
                        stat[1][1] += 1
                    else:
                        stat[1][0] += 1
            else:
                for doc in classification[llr_doc_class]:
                    if t in document[doc]:
                        stat[0][1] += 1
                    else:
                        stat[0][0] += 1

        topper_part = (stat[1][1] + stat[0][1]) / (class_document+other_document)
        bottom_left = stat[1][1] / (stat[1][1] + stat[1][0])
        bottom_right = stat[0][1] / (stat[0][1] + stat[0][0])
        topper = math.pow(topper_part,stat[1][1]) * math.pow(1-topper_part,stat[1][0]) * math.pow(topper_part,stat[0][1]) * math.pow(1-topper_part,stat[0][0])
        bottom = math.pow(bottom_left,stat[1][1]) * math.pow(1-bottom_left,stat[1][0]) * math.pow(bottom_right,stat[0][1]) * math.pow(1-bottom_right,stat[0][0])
        temp_llr_value = (-2) * math.log10(topper/bottom)

        llr_value.append(temp_llr_value)
    return float(sum(llr_value)) / len(llr_value)
