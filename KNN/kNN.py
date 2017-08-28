# coding=utf-8
import numpy as np
import types

def loadData():
    dataFile = open('datingTestSet.txt')
    dataLen = 0
    colMax0 = -1
    colMin0 = 1000000
    colMax1 = -1
    colMin1 = 1000000
    colMax2 = -1
    colMin2 = 1000000
    dataTrain = []
    dataTest = []
    for line in dataFile.readlines():
        lineVec = line.strip().split('\t')
        if dataLen%10 != 0:
            dataTrain.append([float(lineVec[0]),float(lineVec[1]),float(lineVec[2]),float(lineVec[3])])
        else:
            dataTest.append([float(lineVec[0]),float(lineVec[1]),float(lineVec[2]),float(lineVec[3])])
        if colMax0 <= float(lineVec[0]):
            colMax0 = float(lineVec[0])
        if colMin0 >= float(lineVec[0]):
            colMin0 = float(lineVec[0])
        if colMax1 <= float(lineVec[1]):
            colMax1 = float(lineVec[1])
        if colMin1 >= float(lineVec[1]):
            colMin1 = float(lineVec[1])
        if colMax2 <= float(lineVec[2]):
            colMax2 = float(lineVec[2])
        if colMin2 >= float(lineVec[2]):
            colMin2 = float(lineVec[2])
        dataLen += 1
    for row in dataTrain:
        row[0] = (row[0]-colMin0)/(colMax0-colMin0)
        row[1] = (row[1] - colMin1) / (colMax1 - colMin1)
        row[2] = (row[2] - colMin2) / (colMax2 - colMin2)
    for row in dataTest:
        row[0] = (row[0] - colMin0) / (colMax0 - colMin0)
        row[1] = (row[1] - colMin1) / (colMax1 - colMin1)
        row[2] = (row[2] - colMin2) / (colMax2 - colMin2)
    return np.array(dataTrain), np.array(dataTest)

def calDist(inX, inY):
    diff = (inX-inY)**2
    #print (diff)
    dist = diff.sum()
    dist = dist **0.5
    return dist

def vote(data, index):
    cates = data[:,3][index]
    counter = np.array([-1,0,0,0])
    for c in cates:
        counter[int(c)] += 1
    res = counter.argmax()
    return res

def kNN():
     dataTrain, dataTest = loadData()
     num_train = dataTrain.shape[0]
     num_test = dataTest.shape[0]
     right = 0
     #print (num_test)
     for i in range(num_test):
         dist = np.zeros(num_train)
         for j in range(num_train):
             dist[j] = calDist(dataTrain[j][0:3], dataTest[i][0:3])
             #print (dist[j])
         top_index = dist.argsort()[0:20]
         vote_class = vote(dataTrain, top_index)
         # print (vote_class, dataTest[i][3])
         if vote_class == dataTest[i][3]:
             right += 1
     #print ("Total %d hits.")%right
     ratio = right*1.0/num_test
     #print ("Hit ratio is %f")%ratio
     print (right, ratio)


kNN()
