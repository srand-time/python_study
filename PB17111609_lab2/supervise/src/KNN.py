#-*-coding:UTF-8-*-
#from main import *
import functools

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


def mycmp(x,y):
	return x[len(x)-1]-y[len(y)-1]


def cal_distance(data,dataset,k):
#计算某一个数据到 训练集中其他数据的距离(利用的是欧式距离)
#不计算最后一维G3
#并计算训练集,更换不同的k值预测testset中的G3属性（二等级制）
	distance_list=[0.0]*(len(dataset))
	#print(len(dataset[0]))
	for i in range(0,len(dataset)):
		for j in range(0,len(dataset[i])-1):		
			#print(i,j)
			distance_list[i]=distance_list[i]+pow((data[j]-dataset[i][j]),2)
		dataset[i].append(distance_list[i])
	dataset.sort(key=functools.cmp_to_key(mycmp))
	#print(dataset[len(dataset)-1][len(dataset[i])-1])
	#for lists in dataset:
	#	print(lists)
	
	#处理完这个data数据之后删除距离维度
	#因为下次还要用dataset
	for lists in dataset:
		del(lists[len(lists)-1])

	flag=0
	#print(data)
	for i in range(0,k):
		#print(dataset[i])
	#找k个最邻近的点进行预测
		if(dataset[i][len(dataset[i])-1]==0):
			flag=flag-1
		else:
			flag=flag+1
	#print(flag)


	if(flag>0):
	#预测G3是1(合格)
		if(data[len(data)-1]==1):
			return 1
		else:
			return 2
	else:
	#预测不合格
		if(data[len(data)-1]==1):
			return 3
		else:
			return 4

	#for lists in dataset:
	#	print(lists)




def cal_trainset(trainset,testset):
#计算训练集,更换不同的k值预测testset中的G3属性（二等级制）
		true_true_case=0
		false_true_case=0
		true_false_case=0
		false_false_case=0	#实际结果_预测结果
		for data in testset:
			i=cal_distance(data,testset,3)
			if(i==1):
				true_true_case=true_true_case+1
			if(i==2):
				true_false_case=true_false_case+1
			if(i==3):
				false_true_case=false_true_case+1
			if(i==4):
				false_false_case=false_false_case+1
		print('true_true_case,false_true_case,true_false_case,false_false_case',
		true_true_case,false_true_case,true_false_case,false_false_case)

	#cal_distance(testset[0],trainset,3)

#trainset,testset=readcsv(0.7)
#print_data(trainset)
#guiyi(trainset)
#guiyi(testset)
