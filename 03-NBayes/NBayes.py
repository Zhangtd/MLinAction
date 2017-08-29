# coding=utf-8
import random
def textParse(fileString):
    import re
    wordArr = re.split(r'\W*',fileString)
    wordList = [word.lower() for word in wordArr if len(word)>2]
    return wordList

def getText():
    hamInst = []
    spamInst = []

    for i in range(1,26,1):
        filepath1 = 'email/ham/'+str(i)+'.txt'
        filepath2 = 'email/spam/'+str(i)+'.txt'
        file1 = open(filepath1, 'rb')
        file2 = open(filepath2, 'rb')
        hamInst.append(textParse(file1.read()))
        spamInst.append(textParse(file2.read()))
    return hamInst, spamInst

def vocList(instH, instS):
    vocDict = set([])
    for inst in instH:
        vocDict = vocDict | set(inst)
    for inst in instS:
        vocDict = vocDict | set(inst)
    return list(vocDict)

def calWordPro(vocDict, instH, instS):
    total = 2
    wordProH = dict.fromkeys(vocDict,1)
    wordProS = dict.fromkeys(vocDict,1)

    for inst in instH:
        for word in inst:
            wordProH[word] += 1
            total += 1
    for key in wordProH.keys():
        wordProH[key] = wordProH[key]*1.0/total

    total = 2
    for inst in instS:
        for word in inst:
            wordProS[word] += 1
            total += 1
    for key in wordProS.keys():
        wordProS[key] = wordProS[key]*1.0/total

    return wordProH, wordProS

def classify(testInst, wordProH, wordProS):
    from math import log
    proH = 0
    proS = 0
    for word in testInst:
        proH += log(wordProH[word],2)
        proS += log(wordProS[word],2)
    if proH >= proS:
        return 0
    else:
        return 1

def main():
    hamInsts, spamInsts = getText()
    vocDict = vocList(hamInsts, spamInsts)
    wordProH, wordProS = calWordPro(vocDict, hamInsts, spamInsts)
    testH = random.sample(hamInsts, 15)
    testS = random.sample(spamInsts, 10)
    count = 0
    for case in testH:
        pred = classify(case, wordProH, wordProS)
        if pred == 0:
            count += 1
    for case in testS:
        pred = classify(case, wordProH, wordProS)
        if pred == 1:
            count += 1
    print count
if __name__ == '__main__':
    main()

