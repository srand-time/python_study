#-*-coding:UTF-8-*-
#自己选择的机器学习算法---朴素贝叶斯分类算法

#通过所有数据预测G3
#from main import *

def compute_p(list):
#计算   每个正例对应G3及格的概率 每个正例的概率
	res_list=[0 for x in range(0,65)]
	for data in list:
		if(data[32]>0.5):
			res_list[64]=res_list[64]+1
			#G3及格的总数
			for j in range(0,32):
				if(data[j]>0.5):
					res_list[j*2+1]=res_list[j*2+1]+1	#及格下正例总数
		for j in range(0,32):
			if(data[j]>0.5):
				res_list[j*2]=res_list[j*2]+1			#训练样本下正例总数
	return res_list
#返回相当于  某列的数据的正例的个数 对应的让G3及格的个数


def  cal_res(list,total,p_data):
#三个参数分别为 测试列表  训练集的总数据量  概率列表
	true_case=0							#预测正确的数目
	for data in list:
		p=1
		p2=1
		for j in range(0,32):
			if(data[j]>0.5):
				p=p*(p_data[j*2+1]/p_data[64])	#p(因素/及格)n个连乘
				p2=p2*(p_data[j*2]/total)			#p(因素)n个连乘
			else:	#反例下预测及格的概率
				p=p*(p_data[64]-p_data[j*2+1])/(p_data[64])
				p2=p2*(total-p_data[j*2])/total
		#print(p)
		#print(p2)
		#下面的p是算出预测为正例的总概率
		p=(p*(p_data[64]/total))/p2
		#print(p)
		#print("\n\n")
		if(p>0.5):		#预测是及格
			if(data[32]>0.5):#实际上是及格
				true_case=true_case+1
		else:
			if(data[32]<=0.5):#实际上是不及格
				true_case=true_case+1
	print('true_case=,total_case=',true_case,len(list))
#trainset,testset=readcsv(0.7)
#probabilty=compute_p(trainset)
#cal_res(testset,len(trainset),probabilty)
#print(probabilty)

#理论上，朴素贝叶斯模型与其他分类方法相比具有最小的误差率。
#但是实际上并非总是如此，这是因为朴素贝叶斯模型假设属性之间相互独立，这个假设在实际应用中往往是不成立的，
#在属性个数比较多或者属性之间相关性较大时，分类效果不好。
#而在属性相关性较小时，朴素贝叶斯性能最为良好