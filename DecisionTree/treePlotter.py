#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-03 09:24:58
# @Author  : Zhangtd
# @Link    : http://example.org
# @Version : 1
# Decision Tree Plotter
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.5")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def createPlot(myTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks= [], yticks= [])

    createPlot.ax1 = plt.subplot(111, frameon=False ,**axprops)
    plotTree.totalW = float(getNumLeafs(myTree))
    plotTree.totalD = float( getTreeDepth(myTree))
    plotTree.x0ff = -0.5/plotTree.totalW;
    plotTree.y0ff = 1.0
    plotTree(myTree, (0.5,1.0), '')
    #plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    #plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()


def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth += getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
    if thisDepth > maxDepth:
        maxDepth = thisDepth
    return maxDepth


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] + cntrPt[1]) / 2.0
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numleafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)    # depth and width of tree
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.x0ff + (1.0 + float(numleafs)) /
	          2.0 / plotTree.totalW, plotTree.y0ff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.y0ff = plotTree.y0ff - 1.0/plotTree.totalD
    for key in secondDict.keys():
    	if type(secondDict[key]).__name__ == 'dict':
    		plotTree(secondDict[key],cntrPt, str(key))
    	else:
    		plotTree.x0ff = plotTree.x0ff + 1.0/plotTree.totalW
    		plotNode(secondDict[key], (plotTree.x0ff, plotTree.y0ff), cntrPt, leafNode)
    		plotMidText((plotTree.x0ff, plotTree.y0ff), cntrPt, str(key))
    plotTree.y0ff = plotTree.y0ff + 1.0/plotTree.totalD


myTree = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
createPlot(myTree)