#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-26 10:04:56
# @Author  : Zhangtd
# @Version : $Id$
# decision tree in MLinAction
from math import log
import operator


def calcShannonEnt(dataset):
    numEntries = len(dataset)
    labelCounts = {}
    for featVec in dataset:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataset = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataset, labels


def splitDataSet(dataset, axis, val):
    retDataSet = []
    for featVec in dataset:
        if featVec[axis] == val:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeature(dataset):
    numFeature = len(dataset[0]) - 1
    baseEnt = calcShannonEnt(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeature):
        featList = [example[i] for example in dataset]
        uniqueVal = set(featList)
        newEnt = 0.0
        for value in uniqueVal:
            subDataset = splitDataSet(dataset, i, value)
            prob = len(subDataset) / float(len(dataset))
            newEnt += prob * calcShannonEnt(subDataset)
        InfoGain = baseEnt - newEnt
        if(InfoGain > bestInfoGain):
        	bestInfoGain = InfoGain
        	bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
		    classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1), reverse=True)
    Tclass =sortedClassCount[0][0]
    return Tclass


def createTree(dataset,lables):
    classList = [example[-1] for example in dataset]
    if( classList.count(classList[0]) == len(classList) ):
        return classList[0]
    if( len(dataset[0]) == 1 ):
		return majorityCnt(classList)
    bestFeature = chooseBestFeature(dataset)
    bestFeatureLable = lables[bestFeature]
    myTree = {bestFeatureLable:{}}
    del(lables[bestFeature])
    featValues = [example[bestFeature] for example in dataset]
    uniqueVal = set(featValues)
    for val in uniqueVal:
    	subLables = lables[:]
    	subDataset = splitDataSet(dataset , bestFeature ,val)
    	myTree[bestFeatureLable][val] = createTree(subDataset ,subLables)
    return myTree

myData, Lables = createDataSet()
print myData
print Lables
# sEnt = calcShannonEnt(myData)
# print sEnt
# spliteddata = splitDataSet(myData, 0, 0)
# print spliteddata
myTree = createTree(myData ,Lables)
print myTree
