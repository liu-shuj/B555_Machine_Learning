import numpy as np
from typing import *
from functools import reduce

def BagOfWords(doc:List,dictionary:Iterable=None)->dict:
    if dictionary is not None:
        d={item:0 for item in dictionary}
    else:
        d={}
    for word in doc:
        if word not in d:
            if dictionary is None:
                d.update({word:1})
            else:
                raise Exception("Encountered word not in dictionary")
        else:
            d[word]+=1
    return d

def ExtractLDA(n_topics:int,doclist:List[List[str]],n_iters:int=500,alpha:float=None,beta:float=0.01):
    if(alpha is None):
        alpha=5.0/n_topics

    wordlist=[]
    for i_doc in range(0,len(doclist)):
        for word in doclist[i_doc]:
            wordlist.append((word,i_doc))
    np.random.shuffle(wordlist)

    z=[0]*len(wordlist)  # initial topic of each word

    d=set()
    for doc in doclist:
        docdict=set(doc)
        d=d.union(docdict)
    dict_size=len(d)  # number of words in the vocabulary
    dl=list(d)
    d={dl[i]:i for i in range(0,len(dl))}

    C_d=0*np.ndarray((len(doclist),n_topics))
    for i_doc in range(0,len(doclist)):
        C_d[i_doc,0]=len(doclist[i_doc])

    C_t=0*np.ndarray((n_topics,dict_size))
    bigdoc=reduce(lambda x,y:x+y,doclist)
    bow=BagOfWords(bigdoc)
    for word in bow:
        C_t[0,d[word]]=bow[word]

    for iter in range(0,n_iters):
        for i in range(0,len(wordlist)):
            i_word=d[wordlist[i][0]]
            i_doc=wordlist[i][1]
            topic=z[i]
            C_d[i_doc,topic]-=1
            C_t[topic,i_word]-=1
            PD_raw=[]
            for k in range(0,n_topics):
                v1=C_t[k,i_word]+beta
                v2=C_d[i_doc,k]+alpha
                v3=beta*dict_size+C_t[k].sum()
                v4=alpha*n_topics+C_d[i_doc].sum()
                P=v1*v2/(v3*v4)
                PD_raw.append(P)
            # PD_raw=[((C_t[k,i_word]+beta)*(C_d[i_doc,k]+alpha)/((beta*dict_size+C_t[k].sum())*(alpha*n_topics+C_d[i_doc].sum()))) for k in range(0,n_topics)]
            PD=list(map(lambda P:P/sum(PD_raw),PD_raw))
            topic=np.random.choice(range(0,n_topics),p=PD)
            z[i]=topic
            C_d[i_doc,topic]+=1
            C_t[topic,i_word]+=1

    return dl,z,C_d,C_t
