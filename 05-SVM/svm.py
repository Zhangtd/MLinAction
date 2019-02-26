'''

@author: Zhangtd

@contact: zsw@smail.nju.edu.cn

@software: Pycharm 2018

@file: svm.py

@time: 2018/10/24 14:46

@desc:

'''
import numpy as np
import random


def loadData(fileName):
    txt = open(fileName, "r")
    data = []
    label = []
    for line in txt.readlines():
        lineVec = line.strip().split("\t")
        data.append(np.array([float(lineVec[0]), float(lineVec[1])]))
        label.append(np.array([float(lineVec[-1])]))
    return np.array(data), np.array(label)


def selectJ(i, m):
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j


def clipAlpha(aj, H, L):
    if aj>H:
        aj = H
    if aj<L:
        aj = L
    return aj


def smoSimple(data, labels, C, tole, maxIter):
    b = 0
    m, n = data.shape
    alphas = np.zeros((m, 1))
    iter = 0
    while iter < maxIter:
        alphasPairChanged = 0
        for i in range(m):
            y_i = float(np.dot(data[i, :].T, np.dot(data.T, alphas*labels)))+b
            E_i = y_i - float(labels[i])

            # if ((E_i*alphas[i]>tole) and (alphas[i]>0)) or ((E_i*alphas[i]<-tole) and (alphas[i]<C)):
            if ((labels[i] * E_i < -tole) and (alphas[i] < C)) or ((labels[i] * E_i > tole) and (alphas[i] > 0)):
                j = selectJ(i, m)
                y_j = float(np.dot(data[j, :].T, np.dot(data.T, alphas*labels)))+b
                E_j = y_j - float(labels[j])
                if labels[i] != labels[j]:
                    L = max(0, alphas[j]-alphas[i])
                    H = min(C, C+alphas[j]-alphas[i])
                else:
                    L = max(0, alphas[j]+alphas[i]-C)
                    H = min(C, alphas[j]+alphas[i])
                if L == H:
                    print("L==H")
                    continue
                eta = 2.0 * np.dot(data[i,:],data[j,:].T)-np.dot(data[i,:], data[i,:].T)-np.dot(data[j,:], data[j,:].T)
                if eta >= 0:
                    print("eta>=0")
                alphaOldI = alphas[i].copy()
                alphaOldJ = alphas[j].copy()
                alphas[j] -= labels[j]*(E_i-E_j)/eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if abs(alphas[j]-alphaOldJ)<0.00001:
                    print("j not moving enough.")
                    continue
                alphas[i] += labels[j]*labels[i]*(alphaOldJ-alphas[j])
                # print(alphas[i])
                b1 = b - E_i - labels[i]*(alphas[i]-alphaOldI)*np.dot(data[i, :], data[i, :].T) -\
                     labels[j]*(alphas[j]-alphaOldJ)*np.dot(data[i, :], data[j, :].T)
                b2 = b - E_j - labels[i] * (alphas[i] - alphaOldI)*np.dot(data[i, :], data[j, :].T) - \
                     labels[j] * (alphas[j] - alphaOldJ)*np.dot(data[j, :], data[j, :].T)
                if C>alphas[i]>0:
                    b = b1
                elif C>alphas[j]>0:
                    b = b2
                else:
                    b = (b1+b2)/2
                alphasPairChanged += 1
                print("Iter %d, alpha i: %d, changed %d."%(iter, i, alphasPairChanged))
        if alphasPairChanged==0:
            iter += 1
        else:
            iter = 0
        print("iteration %d."%iter)
    return alphas, b


def calWs(alphas, data, labels):
    m, n = data.shape
    ws = np.zeros((1, n))
    for i in range(m):
        ws += alphas[i]*labels[i]*data[i, :]
    return ws


def pred(X, w, b):
    y_ = np.dot(X, w.T)+b
    if float(y_)>0:
        return 1
    else:
        return -1


def eval(Xs, Ys, w, b):
    m, n = Xs.shape
    count = 0
    for i in range(m):
        y_ = pred(Xs[i], w, b)
        if y_ == Ys[i]:
            count += 1
    print("Precision: %.4f"%(count/(m*1.0)))


if __name__ == "__main__":
    data, label = loadData("testSet.txt")
    alphas, b = smoSimple(data, label, 0.6, 0.001, 50)
    ws = calWs(alphas, data, label)
    eval(data, label, ws, b)
