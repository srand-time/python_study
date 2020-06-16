#coding=utf-8
from numpy import *
def readcsv(split):
    with open("wine.data",'r') as file:
        #读取csv文件
        content=file.read()
        dataset=list()
        rows=content.split('\n')
        for row in rows:
            dataset.append(row.split(','))
        #dataset=encoder_char_to_int(dataset)
        del(dataset[len(dataset)-1])
        #guiyi(dataset)
        size=len(dataset)
        print('size=,split=',size,split)
        trainset = dataset[0:int((split/2) * size)]
        trainset2 = dataset[int(size-(split/2)*size):size]
        for set in trainset2:
            trainset.append(set)
        #训练集占split
        testset = dataset[int(split/2 * size):int(size-(split/2)*size)]
        #测试集
        return trainset, testset


def guiyi(dataset):
#归一化处理数据
	max_list=[0]*(len(dataset[0]))
	min_list=[10000]*(len(dataset[0]))
	for i in range(0,len(dataset)):
		for j in range(len(dataset[0])):
			#print(i)
			max_list[j]=max(float(dataset[i][j]),max_list[j])
			min_list[j]=min(float(dataset[i][j]),min_list[j])
	#for j in range(len(dataset[0])-1):
		#print(max_list[j],min_list[j],dataset[0][j])
	for i in range(len(dataset)):
		for j in range(len(dataset[0])):
			dataset[i][j]=(dataset[i][j]-min_list[j])*100/(max_list[j]-min_list[j])


def deal_data(dataset):
#预处理数据
#将第一个字符是'.'的扩展成"0."
#然后还要进行归一化操作
    for i in range(0,len(dataset)):
        if(dataset[i][7][0]=='.'):
            dataset[i][7]="0"+dataset[i][7]
            #print(dataset[i][7])
        if(dataset[i][8][0]=='.'):
            dataset[i][8]="0"+dataset[i][8]
        if(dataset[i][11][0]=='.'):
            dataset[i][11]="0"+dataset[i][11]
        for j in range (0,14):
            dataset[i][j]=float(dataset[i][j])
        del(dataset[i][0])
        #去掉数据的第一维 
    guiyi(dataset)

def print_data(lists):
    i=0
    for list in lists:
        print(list)

def kmeans(k,data):
    #输入参数k是分类数,data是数据集
    #先随机生成k个点
    data_len=len(data[0])
    #print(data_len)
    #center_list=[[0 for i in range(k)] for j in range(data_len)]
    
    center_list=[[0 for i in range(data_len+1)] for j in range(k)]
    #中心点列表
    
    class_list=[0 for i in range(len(data))]
    #对于每个点而言，记录它们分别处于哪一个分类中

    div=k
    #第一次循环的时候，取前k个点当作聚类点
    #相当于随机生成了初始点
    
    for i in range(0,k):
        for j in range(0,data_len):
            center_list[i][j]=data[i][j]
    #print(data[2])
    #print(center_list[2])

    for n in range(0,50):
    #设定循环50次
    #接下来分别计算每个数据点   与中心点的距离（欧式距离）
    #按照与中心点的距离         将每个数据点放入某个类中
        node_class=0    #当前点放入哪一个类中
        min_dist=1000000#当前最小距离
        temp_dist=0     #当前尝试下的距离
        for node in range(0,len(data)):     #遍历所有点
            #print(str(node))
            min_dist=1000000
            for m in range(0,k):            #遍历所有类
                temp_dist=0
                for j in range(0,data_len): #遍历每一维
                    temp_dist=temp_dist+(data[node][j]-center_list[m][j])*(data[node][j]-center_list[m][j])
                    #if node<3:
                     #   print(str(m)+" "+str(temp_dist))
                if(temp_dist<min_dist):
                    node_class=m
                    min_dist=temp_dist
                    #print(str(node_class)+" "+str(min_dist))
            #if node<3 and n==0:
             #   print(node_class)
            class_list[node]=node_class
        #以上计算已经让点分好了类，然后还需要根据分类结果重新计算中心点
        
        for i in range(0,k):
            for j in range(0,data_len+1):
                center_list[i][j]=0

        for i in range(0,len(data)):
            for j in range(0,data_len):
                center_list[class_list[i]][j]=center_list[class_list[i]][j]+data[i][j]
            center_list[class_list[i]][data_len]=center_list[class_list[i]][data_len]+1
        for i in range(0,k):
            for j in range(0,data_len):
                if center_list[i][data_len]!=0:
                    center_list[i][j]=center_list[i][j]/center_list[i][data_len]

    #结束50次循环后打印结果
    print_check(class_list)
    return class_list


def print_check(class_list):
    for i in range(0,178):
        print(class_list[i],end="")
        if(i==58):
            print()
        if(i==129):
            print()

def check(class_list):
    res=0
    for i in range(0,59):
        if(class_list[i]==0):
            res=res+1
    for i in range(59,130):
        if(class_list[i]==1):
            res=res+1
    for i in range(130,178):
        if(class_list[i]==2):
            res=res+1
    print("\ntrue case")
    print(res)


trainset,testset=readcsv(1)
deal_data(trainset)
#h1,h2=pca(trainset,0.5)
print("without pca true case:")
class_list=kmeans(3,trainset)
check(class_list)

#check(class_list)
#pca_list=h1.tolist()
#class_list2=kmeans(3,pca_list)
#print("use pca")
#check(class_list2)
