#encoding="utf-8"
import os
import re
import nltk


def get_filelist(directory, file_list):     # Iteratively search file names
    if os.path.isfile(directory):
        file_list.append(directory)
    elif os.path.isdir(directory):
        for s in os.listdir(directory):
            new_dir = os.path.join(directory, s)
            get_filelist(new_dir, file_list)

    return file_list


def preprocess_files():     # Preprocess files
    datahead = 16
    dataset_addr = r"..\dataset"
    stop_list_addr = r".\stop_list.txt"
    searching_list_addr = r".\searching_list.txt"
    tokenizer = nltk.RegexpTokenizer(r'([A-Za-z0-9]+)')

    stop_list = open(stop_list_addr, 'r').readlines()       # load the stop list
    list_len = len(stop_list)
    for i in range(list_len):
        stop_list[i] = stop_list[i].strip()     
        stop_list[i] = nltk.PorterStemmer().stem(stop_list[i])  # stemming

    searching_list = open(searching_list_addr, 'r').readlines()     # load searching list
    list_len = len(searching_list)
    for i in range(list_len):
        searching_list[i] = re.sub(r'[0-9]+.\t', '', searching_list[i].strip())
        searching_list[i] = re.sub(r'[0-9]+.', '', searching_list[i].strip())
        searching_list[i] = nltk.PorterStemmer().stem(searching_list[i])

    file_list = list()
    files = list()
    file_list = get_filelist(dataset_addr, file_list)
    for x in file_list:
        line_p = open(x, 'r').readlines()[datahead:]
        fp = " ".join(line_p).lower()
        fp = tokenizer.tokenize(fp)     # split words
        list_len = len(fp)
        i = 0
        while i < list_len:
            fp[i] = nltk.PorterStemmer().stem(fp[i])        # stemming
            if fp[i] in stop_list:      # delete stop words
                fp.pop(i)
                list_len -= 1
            else:
                i += 1
        files.append(fp)        # end preprocessing

    return files, searching_list,file_list


def inverted_list(word_list):       # create invested list
    file_seq = -1                   #文件序号
    inverted_dict = dict()
    for sub_list in word_list:
        file_seq += 1
        for element in sub_list:
            if element not in inverted_dict:
                inverted_dict[element] = dict()
                inverted_dict[element][file_seq] = 0
            elif file_seq not in inverted_dict[element]:
                inverted_dict[element][file_seq] = 0
            inverted_dict[element][file_seq] += 1
    #print(inverted_dict)
    output_file = open(r'..\output\inverted_list.txt', 'w+')
    for word in inverted_dict.keys():
        print(word, inverted_dict[word], file=output_file)
    return inverted_dict

def bool_search(inverted_dict,searching_list,file_list):     #布尔搜索，采用and，输入按照src下的searching_list.txt的词表
    #,但是该文件要包含所有searching_list下的词才能搜索出来。输入参数包含逆序表，查询词表，文件名列表
    return_filelist=[]                                      #返回的文件列表序号
    i=0                                                     #当前遍历到第几个文件
    for word in searching_list:
        if i==0:                                        #如果是第一个查询词，把所有出现过该查询词的文件序号加入，之后只需要在这个list中筛选即可。
            for number in inverted_dict[word].keys():           #哪些文件中出现过该查询词
                return_filelist.append(number)
        else:
            return_filelist2=[]
            for number in inverted_dict[word].keys():           #哪些文件中出现过该查询词
                return_filelist2.append(number)
            return_filelist=list(set(return_filelist).intersection(set(return_filelist2)))
        i=i+1
    for number in return_filelist:
        print(file_list[number])
    #print(return_filelist)

my_files, my_searching_list,file_list = preprocess_files()
#print(my_files, my_searching_list)
inverted_dict=inverted_list(my_files)
bool_search(inverted_dict,my_searching_list,file_list)