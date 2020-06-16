#coding=utf-8
from numpy import *

#ͨ������ֵ���ۼƹ����������㽫���ݽ�������ά�ǱȽϺ��ʵģ�
#��������Ĳ���������ֵ�͹�����threshold��������Ҫ������ά����num
def select_eigVals(eigVals,threshold):
    sortArray=sort(eigVals) 
    #ʹ��numpy�е�sort()������ֵ���մ�С��������
    
    sortArray=sortArray[-1::-1] 
    #����ֵ�Ӵ�С����
    arraySum=sum(sortArray) #����ȫ��������ֵ�ܺ�arraySum
    tempSum=0               #ǰnum�����������ĺ�
    num=0
    for i in sortArray:
        tempSum+=i
        num+=1
        if tempSum>=arraySum*threshold:
        #�ҵ���һ��ʹ��ǰnum������������ >= �������������ĺ� * threshold 
            print("select result:"+str(num))
            return num


#pca��������������������dataMat���Ѿ�ת���ɾ���matrix��ʽ�����ݼ����б�ʾ������
#���е�percentage��ʾȡǰ���ٸ�������Ҫ�ﵽ�ķ���ռ�ȣ�Ĭ��Ϊ0.9'''
def pca(dataMat,percentage=0.9):
    meanVals=mean(dataMat,axis=0)  
    #��ÿһ����ƽ��ֵ����ΪЭ����ļ�������Ҫ��ȥ��ֵ
    #axis ������ֵ���� m*n �������ֵ������һ��ʵ��
    #axis = 0��ѹ���У��Ը������ֵ������ 1* n ����
    #axis =1 ��ѹ���У��Ը������ֵ������ m *1 ����
    
    meanRemoved=dataMat-meanVals    
    #��ȥ��ֵ
    
    #print_data(meanRemoved)
    covMat=cov(meanRemoved,rowvar=0)  
    #Numpy�е� cov() ����ֱ����þ����Э�������
    #rowvar=0����ÿһ�д���һ������
    
    #print(covMat)
    eigVals,eigVects=linalg.eig(mat(covMat))  
    #����numpy��Ѱ������ֵ������������ģ��linalg�е�eig()����
    
    k=select_eigVals(eigVals,percentage) 
    #Ҫ�ﵽ�ۼƹ�����percentage����Ҫǰk������
    
    eigValInd=argsort(eigVals)  #������ֵeigVals��С��������
    eigValInd=eigValInd[:-(k+1):-1] #���ź��������ֵ���Ӻ���ǰȡk����������ʵ��ȡ�����k������ֵ
    redEigVects=eigVects[:,eigValInd]   #�������������ֵ��Ӧ����������redEigVects�����ɷ֣�
    lowDDataMat=meanRemoved*redEigVects #��ԭʼ����ͶӰ�����ɷ��ϵõ��µĵ�ά����lowDDataMat
    reconMat=(lowDDataMat*redEigVects.T)#+meanVals   #�õ��ع�����reconMat
    #print_data(meanRemoved)
    #print_data(redEigVects)
    return lowDDataMat,reconMat


def readcsv(split):
    with open("wine.data",'r') as file:
        #��ȡcsv�ļ�
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
        #ѵ����ռsplit
        testset = dataset[int(split/2 * size):int(size-(split/2)*size)]
        #���Լ�
        return trainset, testset
         
def print_data(lists):
    i=0
    for list in lists:
        print(list)

def deal_data(dataset):
#Ԥ��������
#����һ���ַ���'.'����չ��"0."
#Ȼ��Ҫ���й�һ������
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
        #ȥ�����ݵĵ�һά 
    #guiyi(dataset)
  

def guiyi(dataset):
#��һ����������
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
    #������ȫ�����ŵ�[0,1]֮��

    #print_data(trainset)
    pre,res=pca(trainset,0.5)
    print_data(pre)
    #print(pre)

if(debug==True):
    testset=[[-1,-2],[-1,0],[0,0],[2,1],[0,1]]
    h1,h2=pca(testset,0.5)
    print_data(h2)
