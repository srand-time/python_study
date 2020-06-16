#coding=utf-8
from numpy import *

#通过特征值的累计贡献率来计算将数据降到多少维是比较合适的，
#函数传入的参数是特征值和贡献率threshold，返回需要降到的维度数num
def select_eigVals(eigVals,threshold):
    sortArray=sort(eigVals) 
    #使用numpy中的sort()对特征值按照从小到大排序
    
    sortArray=sortArray[-1::-1] 
    #特征值从大到小排序
    arraySum=sum(sortArray) #数据全部的特征值总和arraySum
    tempSum=0               #前num个特征向量的和
    num=0
    for i in sortArray:
        tempSum+=i
        num+=1
        if tempSum>=arraySum*threshold:
        #找到第一个使得前num个特征向量的 >= 所有特征向量的和 * threshold 
            print("select result:"+str(num))
            return num


#pca函数有两个参数，其中dataMat是已经转换成矩阵matrix形式的数据集，列表示特征；
#其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
def pca(dataMat,percentage=0.9):
    meanVals=mean(dataMat,axis=0)  
    #对每一列求平均值，因为协方差的计算中需要减去均值
    #axis 不设置值，对 m*n 个数求均值，返回一个实数
    #axis = 0：压缩行，对各列求均值，返回 1* n 矩阵
    #axis =1 ：压缩列，对各行求均值，返回 m *1 矩阵
    
    meanRemoved=dataMat-meanVals    
    #减去均值
    
    #print_data(meanRemoved)
    covMat=cov(meanRemoved,rowvar=0)  
    #Numpy中的 cov() 可以直接求得矩阵的协方差矩阵。
    #rowvar=0是让每一行代表一个变量
    
    #print(covMat)
    eigVals,eigVects=linalg.eig(mat(covMat))  
    #利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
    
    k=select_eigVals(eigVals,percentage) 
    #要达到累计贡献率percentage，需要前k个向量
    
    eigValInd=argsort(eigVals)  #对特征值eigVals从小到大排序
    eigValInd=eigValInd[:-(k+1):-1] #从排好序的特征值，从后往前取k个，这样就实现取出大的k个特征值
    redEigVects=eigVects[:,eigValInd]   #返回排序后特征值对应的特征向量redEigVects（主成分）
    lowDDataMat=meanRemoved*redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
    reconMat=(lowDDataMat*redEigVects.T)#+meanVals   #得到重构数据reconMat
    #print_data(meanRemoved)
    #print_data(redEigVects)
    return lowDDataMat,reconMat


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
         
def print_data(lists):
    i=0
    for list in lists:
        print(list)

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
    #guiyi(dataset)
  

def guiyi(dataset):
#归一化处理数据
	max_list=[0]*(len(dataset[0]))
	min_list=[1000]*(len(dataset[0]))
	for i in range(0,len(dataset)):
		for j in range(len(dataset[0])):
			#print(i)
			max_list[j]=max(dataset[i][j],max_list[j])
			min_list[j]=min(dataset[i][j],min_list[j])
	#for j in range(len(dataset[0])-1):
		#print(max_list[j],min_list[j],dataset[0][j])
	for i in range(len(dataset)):
		for j in range(len(dataset[0])):
			dataset[i][j]=(dataset[i][j]-min_list[j])/(max_list[j]-min_list[j])


debug=False
if(debug==False):
    trainset,testset=readcsv(1)
    deal_data(trainset)
    guiyi(trainset)
    #将数据全部缩放到[0,1]之内

    #print_data(trainset)
    pre,res=pca(trainset,0.5)
    print_data(pre)
    #print(pre)

if(debug==True):
    testset=[[-1,-2],[-1,0],[0,0],[2,1],[0,1]]
    h1,h2=pca(testset,0.5)
    print_data(h2)
