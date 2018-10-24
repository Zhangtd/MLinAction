'''

@author: Zhangtd

@contact: zsw@smail.nju.edu.cn

@software: Pycharm 2018

@file: svm.py

@time: 2018/10/24 14:46

@desc:

'''
import numpy as np


def loadData(fileName):
    txt = open(fileName, "r")
    data = []
    label = []
    for line in txt.readlines():
        lineVec = line.strip().split("\t")
        data.append(np.array([float(lineVec[0]), float(lineVec[1])]))
        label.append(np.array([float(lineVec[-1])]))
    return np.array(data), np.array(label)


if __name__ == "__main__":
    data, label = loadData("testSet.txt")
    print(data.shape)
    print(label[0])