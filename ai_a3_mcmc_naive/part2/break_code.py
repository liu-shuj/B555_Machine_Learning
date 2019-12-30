#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: Shujun Liu (liushuj)
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#


import random
import math
import copy 
import sys
import encode
import time

probfile="prob"
attempts=6
time_per_attempt=100

# put your code here!
def random_swap(rep,rearr):
    r=random.random()
    if(r<0.5):
        newrep=copy.deepcopy(rep)
        k1,k2=random.sample(list(rep.keys()),2)
        newrep[k1]=rep[k2]
        newrep[k2]=rep[k1]
        newrearr=rearr
    else:
        newrearr=copy.deepcopy(rearr)
        k1,k2=random.sample([0,1,2,3],2)
        newrearr[k1]=rearr[k2]
        newrearr[k2]=rearr[k1]
        newrep=rep
    return newrep,newrearr

def calc_p(doc,pdict,init,end):
    p=0
    for word in doc.split():
        for i in range(0,len(word)-1):
            p+=math.log(pdict[word[i]][word[i+1]])
        p+=init[word[0]]
        p+=end[word[-1]]
    return p
    
def break_code(string, corpus):
    init=dict.fromkeys(list(map(chr, range(ord('a'), ord('z')+1))),0)
    end=dict.fromkeys(list(map(chr, range(ord('a'), ord('z')+1))),0)
    m=dict.fromkeys(list(map(chr, range(ord('a'), ord('z')+1))),dict.fromkeys(list(map(chr, range(ord('a'), ord('z')+1))),0))
    for word in corpus.split():
        for i in range(0,len(word)-1):
            m[word[i]][word[i+1]]+=1
        init[word[0]]+=1
        end[word[-1]]+=1
    for l1 in m:
        total=sum(m[l1].values())
        for l2 in m[l1]:
            m[l1][l2]=m[l1][l2]/total
    suminit=sum(init.values())
    sumend=sum(end.values())
    for l in init:
        init[l]=init[l]/suminit
    for l in end:
        end[l]=end[l]/sumend
    
    counter=0
    cur_max=float("-inf")
    while(counter<attempts):
        counter+=1
        l1=list(range(26))
        l2=list(range(26))
        random.shuffle(l1)
        random.shuffle(l2)
        k=list(map(lambda x:chr(97+x),l1))
        v=list(map(lambda x:chr(97+x),l2))
        reptbl=dict(zip(k,v))
        
        rearrtbl=list(range(4))
        random.shuffle(rearrtbl)
        start=time.time()
        elapsed=0
        while(elapsed<time_per_attempt):
            newrep,newrearr=random_swap(reptbl,rearrtbl)
            d1=encode.encode(string,reptbl,rearrtbl)
            d2=encode.encode(string,newrep,newrearr)
            p1=calc_p(d1,m,init,end)
            p2=calc_p(d2,m,init,end)
            if(p2>p1):
                reptbl=newrep
                rearrtbl=newrearr
            else:
                r=random.random()
                if(r<math.exp(p2-p1)):
                    reptbl=newrep
                    rearrtbl=newrearr
            if(p2>cur_max):
                cur_max=p2
                cur_best=d2
            elapsed=time.time()-start
        print("Attempt {num}:\n Current best guess: {cur_best}, logP={cur_max}...".format(num=counter,cur_best=cur_best,cur_max=cur_max))
    return cur_best


if __name__== "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")
    random.seed()
    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded, corpus)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)

