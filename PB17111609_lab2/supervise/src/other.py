#-*-coding:UTF-8-*-
#�Լ�ѡ��Ļ���ѧϰ�㷨---���ر�Ҷ˹�����㷨

#ͨ����������Ԥ��G3
#from main import *

def compute_p(list):
#����   ÿ��������ӦG3����ĸ��� ÿ�������ĸ���
	res_list=[0 for x in range(0,65)]
	for data in list:
		if(data[32]>0.5):
			res_list[64]=res_list[64]+1
			#G3���������
			for j in range(0,32):
				if(data[j]>0.5):
					res_list[j*2+1]=res_list[j*2+1]+1	#��������������
		for j in range(0,32):
			if(data[j]>0.5):
				res_list[j*2]=res_list[j*2]+1			#ѵ����������������
	return res_list
#�����൱��  ĳ�е����ݵ������ĸ��� ��Ӧ����G3����ĸ���


def  cal_res(list,total,p_data):
#���������ֱ�Ϊ �����б�  ѵ��������������  �����б�
	true_case=0							#Ԥ����ȷ����Ŀ
	for data in list:
		p=1
		p2=1
		for j in range(0,32):
			if(data[j]>0.5):
				p=p*(p_data[j*2+1]/p_data[64])	#p(����/����)n������
				p2=p2*(p_data[j*2]/total)			#p(����)n������
			else:	#������Ԥ�⼰��ĸ���
				p=p*(p_data[64]-p_data[j*2+1])/(p_data[64])
				p2=p2*(total-p_data[j*2])/total
		#print(p)
		#print(p2)
		#�����p�����Ԥ��Ϊ�������ܸ���
		p=(p*(p_data[64]/total))/p2
		#print(p)
		#print("\n\n")
		if(p>0.5):		#Ԥ���Ǽ���
			if(data[32]>0.5):#ʵ�����Ǽ���
				true_case=true_case+1
		else:
			if(data[32]<=0.5):#ʵ�����ǲ�����
				true_case=true_case+1
	print('true_case=,total_case=',true_case,len(list))
#trainset,testset=readcsv(0.7)
#probabilty=compute_p(trainset)
#cal_res(testset,len(trainset),probabilty)
#print(probabilty)

#�����ϣ����ر�Ҷ˹ģ�����������෽����Ⱦ�����С������ʡ�
#����ʵ���ϲ���������ˣ�������Ϊ���ر�Ҷ˹ģ�ͼ�������֮���໥���������������ʵ��Ӧ���������ǲ������ģ�
#�����Ը����Ƚ϶��������֮������Խϴ�ʱ������Ч�����á�
#������������Խ�Сʱ�����ر�Ҷ˹������Ϊ����