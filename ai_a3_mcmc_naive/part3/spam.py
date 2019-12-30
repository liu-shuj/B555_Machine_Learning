# Author: Shujun Liu (liushuj)

import os
import sys
import math

enable_acc=1

train=sys.argv[1]
test=sys.argv[2]
out=sys.argv[3]

scnt={}
for filename in os.listdir(os.path.join(train,"spam")):
    with open(os.path.join(train,"spam",filename),'r') as f:
        try:
            seen=set()
            text=f.read()
            text=text.lower()
            l=text.split()
            l=list(map(str.strip,l))
            for w in l:
                if w not in seen:
                    if w in scnt:
                        scnt[w]+=1
                    else:
                        scnt[w]=1
                    seen.add(w)
        except:
            pass

nscnt={}
for filename in os.listdir(os.path.join(train,"notspam")):
    with open(os.path.join(train,"notspam",filename),'r') as f:
        try:
            seen=set()
            text=f.read()
            text=text.lower()
            l=text.split()
            l=list(map(str.strip,l))
            for w in l:
                if w not in seen:
                    if w in nscnt:
                        nscnt[w]+=1
                    else:
                        nscnt[w]=1
                    seen.add(w)
        except:
            pass
                
for w in scnt:
    if w not in nscnt:
        nscnt[w]=0
        
for w in nscnt:
    if w not in scnt:
        scnt[w]=0
        
pw_s={}
pw_ns={}
ssize=len(os.listdir(os.path.join(train,"spam")))
for w in scnt:
    pw_s[w]=scnt[w]/ssize
nssize=len(os.listdir(os.path.join(train,"notspam")))
for w in nscnt:
    pw_ns[w]=nscnt[w]/nssize
    
res={}
for filename in os.listdir(test):
    with open(os.path.join(test,filename),'r') as f:
        try:
            text=f.read()
            text=text.lower()
            l=text.split()
            l=list(map(str.strip,l))
            ps=0
            pns=0
            for w in l:
                if(w in scnt):
                    if(scnt[w]>0):
                        ps+=math.log(scnt[w])
                    if(nscnt[w]>0):
                        pns+=math.log(nscnt[w])
            if(ps>pns):
                res[filename]=1
            else:
                res[filename]=0
        except:
            res[filename]=1
            
with open(out,'w') as f:
    for key,value in res.items():
        if(value==1):
            f.write(key+" spam\n")
        else:
            f.write(key+" notspam\n")
            
print("Results written to '{out}'...".format(out=out))

if(enable_acc==1):
    correct=0
    total=0
    with open("test-groundtruth.txt",'r') as f:
        for line in f:
            total+=1
            pair=line.strip().split(" ")
            if((pair[1]=='spam' and res[pair[0]]==1) or (pair[1]=='notspam' and res[pair[0]]==0)):
                correct+=1
    print("Accuracy is {acc}...".format(acc=correct/total))