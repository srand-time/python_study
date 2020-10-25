# exp1

## 1. 运行环境

	Pycharm, Python3.7/Python3.8



## 2. 编译运行方式

	python bool_search.py
	python semantic_search.py



## 3.一些说明

#### 文件说明

```
src/stop_list.txt----停用词表
src/searching_list.txt-----查询词表，即输入文件
dataset下任意的文件结构都可以，因为是迭代读取的

output/inverted_list.txt是倒排表，是以二重字典的形式存储的。第一层字典的key是单词，对应的value是第二层字典。第二层字典的key是文件序号，value是该文件中单词出现的次数。

output/tf-idf.txt是tf-idf矩阵。采用了自己的简单压缩方式，即直接标明该值所处的位置。比如a[1][2]=
0.123,会直接显示为 1,2：0.123。
```

#### 运行说明

```
布尔检索时采用的是and，需要查询在一个文件中查询到查询词表中的所有查询词才会检索到该文件。
运行需要一定时间，请耐心等待。
```



## 4. 关键函数

#### 公共部分：

```python
get_filelist()	#迭代读取output下所有的文件

preprocess_files()	#预处理。将所有文件都读出来，并进行词根化，去掉停用词的处理。
					#最后得到一个二重列表，第一维相当于是第几个文件，第二维的列表中
    				#以单词的形式显示预处理之后文件的所有内容
```

#### 布尔检索：

```python
inverted_list()	#构建逆排表，形式为二维字典
bool_search()	#布尔检索，遍历查询词，对于每一个查询词，构建一个list包含所有出现过该查询词的文件，之后取并集即可。
```

#### 语义检索：

```python
def word_of_files(my_files):      #统计出现过的所有词，形成一个字典（词-->序号）
def file_word_freq(my_files,word_dict):      #文件中单词出现的次数表
def TF_IDF(f_w_freq,my_files,word_dict):	#构建TF_IDF矩阵
search()		#搜索函数，按照余弦相似度计算之后选出10个最相似的。
```

