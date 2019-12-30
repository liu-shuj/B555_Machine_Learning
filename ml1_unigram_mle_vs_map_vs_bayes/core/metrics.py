import math

def CalcPP(tokenSeq,prDict)->float:
    sum=0
    N=0
    for token in tokenSeq:
        N+=1
        try:
            if prDict[token]==0:
                return float("inf")
            sum+=math.log(prDict[token])
        except KeyError:
            print("Token {token} is not in dictionary. Ignoring...".format(token=token))
    PP=math.exp(-sum/N)
    return PP

