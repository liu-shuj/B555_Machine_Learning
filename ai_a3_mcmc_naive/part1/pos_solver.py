###################################
# CS B551 Fall 2019, Assignment #3
#
# Your names and user ids: Shujun Liu (liushuj)
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
from numpy import *

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            res=0
            for wi,si in zip(sentence,label):
                if(si in self.pw_s):
                    if(wi in self.pw_s[si]):
                        res+=math.log(self.pw_s[si][wi])
                        res+=math.log(self.p_s[si])
                    else:
                        res=float("-inf")
            return res
        elif model == "Complex":
            return -999
        elif model == "HMM":
            res=self.p1st[label[0]]+self.pw_s[label[0]][sentence[0]]
            for i in range(1,len(sentence)):
                res+=self.ps_s[label[i-1]][label[i]]
                if(sentence[i] in self.pw_s[label[i]]):
                    res+=self.pw_s[label[i]][sentence[i]]
            return res            
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        cnts_w={}
        cntw_s={}
        cnts_s={}
        cnt1st={}
        cnt_s={}
        for (s,gt) in data:
            if(gt[0] not in cnt1st):
                cnt1st[gt[0]]=1
            else:
                cnt1st[gt[0]]+=1
            for wi,si in zip(s,gt):
                if(wi in cnts_w):
                    if(si in cnts_w[wi]):
                        cnts_w[wi][si]+=1
                    else:
                        cnts_w[wi][si]=1
                else:
                    cnts_w[wi]={}
                    cnts_w[wi][si]=1
                if(si in cntw_s):
                    if(wi in cntw_s[si]):
                        cntw_s[si][wi]+=1
                    else:
                        cntw_s[si][wi]=1
                else:
                    cntw_s[si]={}
                    cntw_s[si][wi]=1
                if(si in cnt_s):
                    cnt_s[si]+=1
                else:
                    cnt_s[si]=1
            for i in range(0,len(gt)-1):
                scur=gt[i]
                sn=gt[i+1]
                if(scur in cnts_s):
                    if(sn in cnts_s[scur]):
                        cnts_s[scur][sn]+=1
                    else:
                        cnts_s[scur][sn]=1
                else:
                    cnts_s[scur]={}
                    cnts_s[scur][sn]=1
        maxs_w={}
        for w in cnts_w:
            maxs_w[w]=max(cnts_w[w],key=lambda k:cnts_w[w][k])
        self.maxs_w=maxs_w
        
        pw_s=dict.fromkeys(cntw_s,{})
        for s in pw_s:
            total=sum(list((cntw_s[s]).values()))
            for w in cntw_s[s]:
                pw_s[s][w]=cntw_s[s][w]/total
        self.pw_s=pw_s
                
        ps_s=dict.fromkeys(cnts_s,{})
        for k1 in cnts_s:
            for k2 in cnts_s:
                if k2 not in cnts_s[k1]:
                    cnts_s[k1][k2]=0
        for s1 in ps_s:
            total=sum(list(cnts_s[s1].values()))
            for s2 in cnts_s:
                ps_s[s1][s2]=cnts_s[s1][s2]/total
        self.ps_s=ps_s
        self.all_s=list(ps_s.keys())
        
        p1st=dict.fromkeys(cnt1st,0)
        for s in p1st:
            p1st[s]=cnt1st[s]/sum(list(cnt1st.values()))
        self.p1st=p1st
        
        p_s=dict.fromkeys(cnt_s,0)
        for s in p_s:
            p_s[s]=cnt_s[s]/sum(list(cnt_s.values()))
        self.p_s=p_s
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        res=[]
        for w in sentence:
            if w in self.maxs_w:
                res.append(self.maxs_w[w])
            else:
                res.append(random.choice(self.all_s))
        return res

    def complex_mcmc(self, sentence):
        return [ "noun" ] * len(sentence)

    def hmm_viterbi(self, sentence):
        ep=zeros((len(self.all_s),len(sentence)))
        for i in range(len(sentence)):
            for j in range(len(self.all_s)):
                if(sentence[i] not in self.pw_s[self.all_s[j]]):
                    ep[j,i]=0
                else:
                    ep[j,i]=self.pw_s[self.all_s[j]][sentence[i]]
        lep=ma.log(ep).filled(-inf)
        ns=len(self.all_s)
        ltp=(-inf)*ones((ns,ns))
        for i in range(ns):
            for j in range(ns):
                ltp[i,j]=log(self.ps_s[self.all_s[i]][self.all_s[j]])
        lv=zeros((ns,len(sentence)))
        p0=zeros(ns)
        for i in range(ns):
            p0[i]=self.p1st[self.all_s[i]]
        lv[:,0]=lep[:,0]+log(p0)
        r=zeros((ns,len(sentence)))
        
        for i in range(1,len(sentence)):
            vp=lv[:,i-1]+ltp.T
            r[:,i]=argmax(vp,1)
            lv[:,i]=lep[:,i]+vp.max(1)
        path=[]
        cols=len(sentence)
        prev=int(r[argmax(lv[:,cols-1]),cols-1])
        path.append(argmax(lv[:,cols-1]))
        path.append(prev)
        i=cols-2
        while(i>0):
            prev=int(r[prev,i])
            path.append(prev)
            i=i-1
        path.reverse()
        res=[]
        for i in path:
            res.append(self.all_s[i])
        return res


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

