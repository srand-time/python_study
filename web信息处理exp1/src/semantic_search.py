#encoding="utf-8"
import os
import re
import nltk
from numpy import array
import math 

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


def word_of_files(my_files):      #统计出现过的所有词，形成一个字典（词-->序号）
                                  #如果不统计，那么无法确定矩阵大小。所以我只能遍历两次。
    word_dict = dict()
    i=0
    for files in my_files:
        for word in files:
            if word not in word_dict.keys():
                word_dict[word]=i
                i=i+1
    return word_dict


def file_word_freq(my_files,word_dict):      #文件中单词出现的次数表
    f_w_freq= [[0 for j in range(0,len(word_dict) )] for i in range(0,len(my_files) )]
    i=0
    for files in my_files:
        for word in files:
            f_w_freq[i][word_dict[word]]+=1          
        i=i+1
    return f_w_freq


#TF（Term Frequency）表示某个关键词在整篇文章中出现的频率。每个单词的词频/整个文章的单词总数
#IDF（InversDocument Frequency）表示计算倒文本频率。文本频率是指某个关键词在整个语料所有文章中出现的次数。
# 倒文档频率又称为逆文档频率，它是文档频率的倒数，主要用于降低所有文档中一些常见却对文档影响不大的词语的作用。
def TF_IDF(f_w_freq,my_files,word_dict):
    tf_idf=[[0 for j in range(0,len(word_dict) )] for i in range(0,len(my_files) )] #每个文档的每个单词的TF-IDF值
    IDF=[0 for i in range(0,len(word_dict))]                     #每个单词的IDF值
    contain_word=[0 for i in range(0,len(word_dict))]            #每个单词在多少个文档中出现过
    i=0         #当前遍历到哪一个文件
    for files in my_files:
        for j in range(0,len(word_dict)):
            if f_w_freq[i][j]!=0:
                contain_word[j]+=1
        i=i+1
    #print(contain_word)

    i=0
    for files in my_files:
        if len(files)==0:
            break
        for j in range(0,len(word_dict)):
            TF=f_w_freq[i][j]/len(files)
            IDF[j]=math.log(  len(my_files)/(contain_word[j]+1) )#log[文章总数/(包含该词的文章数目+1)]
            tf_idf[i][j]=TF*IDF[j]
        i=i+1
    
    output_file = open(r'..\output\tf-idf.txt', 'w+')
    for i in range(0,len(my_files)):
        for j in range(0,len(word_dict)):
            if tf_idf[i][j]!=0:
                print(i,",",j,":","%0.5f"%tf_idf[i][j],end="\t",file=output_file)
        print("\n",file=output_file)
    return tf_idf,IDF


def search(tf_idf,my_searching_list,word_dict,file_list,idf):       #搜索函数
    #print(my_searching_list)
    search_vector=[0 for i in range(0,len(word_dict))]          #搜索向量
    similar_vector=[0 for i in range(0,len(file_list))]         #相似度数组  
    word_num=0                      #该搜索项中出现过的单词总数
    for word in my_searching_list:
        if word in word_dict:
            search_vector[word_dict[word]]=1
            word_num=word_num+1
    for j in range(0,len(word_dict)):
        TF=search_vector[j]/word_num
        search_vector[j]=TF*idf[j]
    #print(search_vector)
    #利用余弦向量公式计算相似度
    for i in range(0,len(file_list)):
        A_MUT_B=0       #记录Ai*Bi的和
        sum_abs_A=0     #记录Ai的绝对值的和
        sum_abs_B=0     #记录Bi的绝对值的和
        for j in range(0,len(word_dict)):
            A_MUT_B+=search_vector[j]*tf_idf[i][j]
            sum_abs_A+=abs(search_vector[j])
            sum_abs_B+=abs(tf_idf[i][j])
        similar_vector[i]=A_MUT_B/(sum_abs_A+sum_abs_B)
    
    #选出10个最相似的
    has_selected=[]     #已经被挑出来的文件
    if(len(file_list)<10):
        print("number of file less than 10")
    else:
        for i in range(0,10):
            max_val=-10000
            max_index=0
            for j in range(0,len(similar_vector)):
                if j not in has_selected and max_val<similar_vector[j]:
                    max_val=similar_vector[j]
                    max_index=j
            has_selected.append(max_index)
            print(file_list[max_index])


my_files, my_searching_list,file_list = preprocess_files()  #my_files是进行过预处理的文件组织成的列表。
word_dict=word_of_files(my_files)
f_w_freq=file_word_freq(my_files,word_dict)
tf_idf,idf=TF_IDF(f_w_freq,my_files,word_dict)
search(tf_idf,my_searching_list,word_dict,file_list,idf)