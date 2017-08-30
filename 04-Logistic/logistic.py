# coding = utf-8
import numpy as np
import types
def loadData():
    fileTrain = open('horseColicTraining.txt','rb')
    fileTest = open('horseColicTest.txt','rb')
    dataTrain = []
    dataTest = []
    for line in fileTrain.readlines():
        lineVec = line.strip().split('\t')
        arr = []
        for item in lineVec:
            arr.append(float(item))
        dataTrain.append(arr)
    for line in fileTest.readlines():
        lineVec = line.strip().split('\t')
        arr = []
        for item in lineVec:
            arr.append(float(item))
        dataTest.append(arr)
    return dataTrain, dataTest

def sigmoid(inX):
    from math import exp
    res = []
    for x in inX:
        res.append(1.0/(1+exp(-x)))
    return np.array(res)

def gradAscend(data):
    featCols = []
    labels = []
    alpha = 0.05
    maxIter = 1000

    for row in data:
        featCols.append(row[0:-1])
        labels.append(row[-1])
    featMat = np.array(featCols)
    labelMat = np.array(labels)

    weights = np.random.random((featMat.shape[1],))

    for i in range(maxIter):
        z = np.dot(featMat,weights)
        error = labelMat - sigmoid(z)
        print error
        weights = weights + alpha * np.dot(featMat.transpose(),error)
        print weights

dataTrain, dataTest = loadData()
gradAscend(dataTrain)