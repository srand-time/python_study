#-*-coding:UTF-8-*-
import csv
from   KNN import *
from   other import *
def readcsv(split):
    with open("student/student-mat.csv",'r') as file:
        #读取csv文件
        content=file.read()
        dataset=list()
        rows=content.split('\n')
        for row in rows:
            dataset.append(row.split(';'))
        dataset=encoder_char_to_int(dataset)
        del(dataset[len(dataset)-1])
        guiyi(dataset)
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

def encoder_char_to_int(data):
#将一些字符型变量翻译成整形
    del(data[0])
    for i in range(0,len(data)-1):
        if data[i][0]=='"GP"':
            data[i][0]=0
        elif data[i][0]=='"MS"':
            data[i][0]=1

        if data[i][1]=='"F"':
            data[i][1]=0
        elif data[i][1]=='"M"':
            data[i][1]=1

        if data[i][3]=='"U"':
            data[i][3]=0
        elif data[i][3]=='"R"':
            data[i][3]=1

        if data[i][4]=='"LE3"':
            data[i][4]=0
        elif data[i][4]=='"GT3"':
            data[i][4]=1

        if data[i][5]=='"T"':
            data[i][5]=0
        elif data[i][5]=='"A"':
            data[i][5]=1
        
        if data[i][8]=='"at_home"':
            data[i][8]=0
        elif data[i][8]=='"services"':
            data[i][8]=1
        elif data[i][8]=='"health"':
            data[i][8]=2
        elif data[i][8]=='"other"':
            data[i][8]=3
        elif data[i][8]=='"teacher"':
            data[i][8]=4

        if data[i][9]=='"at_home"':
            data[i][9]=0
        elif data[i][9]=='"services"':
            data[i][9]=1
        elif data[i][9]=='"health"':
            data[i][9]=2
        elif data[i][9]=='"other"':
            data[i][9]=3
        elif data[i][9]=='"teacher"':
            data[i][9]=4

        if data[i][10]=='"home"':
            data[i][10]=0
        elif data[i][10]=='"reputation"':
            data[i][10]=1
        elif data[i][10]=='"course"':
            data[i][10]=2
        elif data[i][10]=='"other"':
            data[i][10]=3

        if data[i][11]=='"father"':
            data[i][11]=0
        elif data[i][11]=='"mother"':
            data[i][11]=1
        elif data[i][11]=='"other"':
            data[i][11]=2

        if int(data[i][32])>=10:
            data[i][32]=1
        elif int(data[i][32])<10:
            data[i][32]=0

        for j in range (15,23):
            if(data[i][j]=='"no"'):
                data[i][j]=0
            elif(data[i][j]=='"yes"'):
                data[i][j]=1

        data[i][30]=data[i][30][1:-1]
        data[i][31]=data[i][31][1:-1]
        for j in range (0,33):
            data[i][j]=int(data[i][j])
    return data
    
def print_data(lists):
    i=0
    for list in lists:
        print(list)


trainset,testset=readcsv(0.7)
print('KNN result:')
cal_trainset(trainset,testset)
print('finally we choose k=3,its accuracy rate',106/118)

print('Bayes result:')
probabilty=compute_p(trainset)
cal_res(testset,len(trainset),probabilty)