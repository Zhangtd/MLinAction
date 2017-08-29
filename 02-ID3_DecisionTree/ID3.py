# coding=utf-8
import pickle
def loadData(filename):
    file_data = open(filename,'r')
    datas = [line.strip().split('\t') for line in file_data.readlines()]
    return datas

def calEnt(dataSet):
    from math import log
    total = len(dataSet)
    count = {}
    for inst in dataSet:
        if inst[-1] not in count.keys():
            count[inst[-1]] = 0
        count[inst[-1]] += 1
    ent = 0
    for key in count.keys():
        pro = count[key]*1.0/total
        pro_log = log(pro,2)
        ent += pro * pro_log
    return -ent

def bestSplit(dataSet, cur_labels):
    total = len(dataSet)
    old_ent = calEnt(dataSet)
    num_lables = len(cur_labels)
    dataSplited = {}
    new_ents = [0.0 for i in range(num_lables)]
    for i in range(num_lables):
        dataSplited[i] = {}
        for inst in dataSet:
            if inst[i] not in dataSplited[i].keys():
                dataSplited[i][inst[i]] = []
            dataSplited[i][inst[i]].append(inst)
        for key in dataSplited[i].keys():
            weight = len(dataSplited[i][key])*1.0/total
            ent = calEnt(dataSplited[i][key])
            new_ents[i] += weight*ent
    maxGain = -100
    gainIndex = -1
    for i in range(num_lables):
        if maxGain <= (old_ent-new_ents[i]):
            gainIndex = i
    for key in dataSplited[gainIndex].keys():
        for inst in dataSplited[gainIndex][key]:
            del inst[gainIndex]
    bestFeat = cur_labels[gainIndex]
    del cur_labels[gainIndex]
    return dataSplited[gainIndex], cur_labels, bestFeat

def createTree(dataSet, cur_labels):
    DTree = {}
    for key in dataSet.keys():
        labelCount = {}
        cur_label = [label for label in cur_labels]
        for inst in dataSet[key]:
            if inst[-1] not in labelCount.keys():
                labelCount[inst[-1]] = 0
            labelCount[inst[-1]] += 1
        maxCount = -1
        for label in labelCount.keys():
            if maxCount <= labelCount[label]:
                maxCount = labelCount[label]
                maxLabel = label
        if cur_label == [] or maxCount == len(dataSet[key]):
            DTree[key] = maxLabel
        else:
            newData, newLabels, bestFeat = bestSplit(dataSet[key], cur_label)
            subTree = {}
            subTree[bestFeat] = createTree(newData, newLabels)
            DTree[key] = subTree
    return DTree

def saveTree(myTree):
    path = 'tree.pkl'
    file1 = open(path,'wb')
    pickle.dumps(myTree,file1)
    print ("Saving Completed.")
    file1.close()

filename = 'lenses.txt'
labels = ['age', 'prescript', 'astigmatic', 'tearRate']
wholeData = loadData(filename)

ent = calEnt(wholeData)
Tree = {}
newData, newLabels, bestFeat = bestSplit(wholeData,labels)
Tree[bestFeat] = createTree(newData,newLabels)
print(Tree)
#saveTree(Tree)
