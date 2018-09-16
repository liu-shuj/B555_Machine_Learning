from fractions import Fraction
from scipy.special import gammaln  # fast and specialized but needs scipy

def TrainMLE(tokenSeq,wordList)->dict:
    size = 0
    muDict = {}
    for word in wordList:
        muDict[word]=0
    for token in tokenSeq:
        size+=1  # actual size of the sequence
        muDict[token]+=1  # frequency, as numerator
    for key in muDict:  # add-one smoothing
        if muDict[key]==0:
            muDict[key]=1
            size+=1
    for key in muDict:
        muDict[key]=Fraction(muDict[key],size)
    return muDict

def TrainMAP(tokenSeq,alphaDict)->dict:
    K = len(alphaDict)
    size = 0
    alpha0 = sum(alphaDict.values())
    muDict={}
    for word in alphaDict:
        muDict[word]=alphaDict[word]-1  # initial numerator
    for token in tokenSeq:
        size+=1
        muDict[token]+=1  # increasing numerator
    denom = alpha0 + size - K
    for key in muDict:
        muDict[key]=Fraction(Fraction(muDict[key]),Fraction(denom))
    return muDict

def TrainPD(tokenSeq,alphaDict)->dict:
    K = len(alphaDict)
    size = 0
    alpha0 = sum(alphaDict.values())
    prDict = {}
    for word in alphaDict:
        prDict[word]=alphaDict[word]  # initial numerator
    for token in tokenSeq:
        size+=1
        prDict[token]+=1  # increasing numerator
    denom=size+alpha0
    for key in prDict:
        prDict[key]=Fraction(Fraction(prDict[key]),Fraction(denom))
    return prDict

def LogEvidence(tokenSeq, alphaDict) -> float:
    freqDict = {}
    for word in alphaDict:
        freqDict[word] = 0
    N=0
    for token in tokenSeq:
        N+=1
        freqDict[token] += 1
    K = len(alphaDict)
    alpha0 = sum(alphaDict.values())
    logL=gammaln(alpha0)
    logR=gammaln(alpha0+N)
    for word in alphaDict:
        logL+=gammaln(alphaDict[word]+freqDict[word])
        logR+=gammaln(alphaDict[word])
    logEvidence = logL-logR
    return logEvidence