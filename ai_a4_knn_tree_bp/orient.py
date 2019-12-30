from sys import argv
import numpy as np
import scipy
from scipy import stats
from scipy import spatial
from scipy import special
from scipy.spatial.distance import correlation
from scipy.special import expit
import pickle
import shutil

k=20

tree_feats=192
n_trees=512
n_samples=1024
classes=[0,90,180,270]

bp_iters=5
width=180
alpha=0.00015
outs=4

def build_tree(data,labels):
    if(np.all(labels==labels[0])):
        return [labels[0]]
    if(data.size==0):
        return [scipy.stats.mode(labels)[0][0]]
    n=len(labels)
    HS=0
    for c in classes:
        pc=(np.count_nonzero(labels==c))/n
        if(pc!=0):
            HS=HS-pc*np.log2(pc)
    curmaxIG=-np.inf
    for i in range(data.shape[1]):
        IG=HS
        col=data[:,i]
        for t in [True,False]:
            Ht=0
            lt=labels[col==t]
            if(lt.size>0):
                for c in classes:
                    pc=(np.count_nonzero(lt==c))/len(lt)
                    if(pc!=0):
                        Ht=Ht-pc*np.log2(pc)
            pt=(np.count_nonzero(col==t))/n
            if(pt!=0):
                IG=IG-pt*Ht
        if(IG>curmaxIG):
            curmaxIG=IG
            best=i
    if(curmaxIG<=0):
        return ["random",list(np.unique(labels))]
    return [best,build_tree(np.delete(data[data[:,best]==True],best,1),labels[data[:,best]==True]),build_tree(np.delete(data[data[:,best]==False],best,1),labels[data[:,best]==False])]
        
def train_forest(data,labels):
    feats=np.arange(data.shape[1])
    cp=[]
    for i in range(len(feats)):
        for j in range(i+1,len(feats)):
            cp.append([feats[i],feats[j]])
    cp=np.array(cp)
    trees=[]
    for i in range(n_trees):
        partind=np.random.choice(data.shape[0],n_samples,replace=False)
        partdata=data[partind]
        partlabels=labels[partind]
        print("Training tree " + str(i+1) + "...")
        pairs=cp[np.random.choice(cp.shape[0],tree_feats,replace=False)]
        newdata=((np.diff(partdata.T[pairs],axis=1)>0).T)[:,0]
        trees.append((pairs,build_tree(newdata,partlabels)))
    return trees

def tree_predict(tree,sample):
    if(len(tree)==2 and tree[0]=="random"):
        return np.random.choice(tree[1])
    if(len(tree)==1):
        return tree[0]
    return tree_predict(tree[1],sample) if sample[tree[0]] else tree_predict(tree[2],sample)    
    
def dsigmoid(x):
    return expit(x)*(1-expit(x))
    
def softmax(x):
    return (np.exp(x))/np.sum(np.exp(x))
    
def dsoftmax(x):
    return softmax(x)*(1-softmax(x))    
    
def train_net(data,labels):
    w0=np.random.randn(data.shape[1],width)
    w1=np.random.randn(width,outs)
    for iter in range(bp_iters):
        for i in range(data.shape[0]):
            o1=expit(data[i].dot(w0))
            out=softmax(o1.dot(w1))
            dout=dsoftmax(out)*(labels[i]-out)
            d1=dsoftmax(o1)*(w1.dot(dout))
            w0+=alpha*np.outer(data[i],d1)
            w1+=alpha*np.outer(o1,dout)
    return w0,w1
        

def train(data,modelfile,model):
    if(model=="best"):
        model="nearest"
    if(model=="nearest"):
        with open(data,'r') as f:
            a=[]
            for line in f:
                l=line.split()
                a.append(list(map(int,l[1:])))
        a=np.array(a)
        with open(modelfile,"wb") as f:
            np.save(f,a)                
    elif(model=="tree"):
        with open(data,'r') as f:
            a=[]
            labels=[]
            for line in f:
                l=line.split()
                a.append(list(map(int,l[2:])))
                labels.append(int(l[1]))
        d=np.array(a)
        labels=np.array(labels)
        forest=train_forest(d,labels)
        with open(modelfile,'wb') as f:
            pickle.dump(forest,f)
    elif(model=="nnet"):
        with open(data,'r') as f:
            a=[]
            labels=[]
            for line in f:
                l=line.split()
                a.append(list(map(int,l[2:])))
                lbl=0
                if(l[1]==90):
                    lbl=1
                elif(l[1]==180):
                    lbl=2
                elif(l[1]==270):
                    lbl=3
                labels.append(lbl)
        d=np.array(a)
        labels=np.array(labels)
        net=train_net(d,labels)
        with open(modelfile,'wb') as f:
            pickle.dump(net,f)
                
def test(data,modelfile,model):
    if(model=="best"):
        model="nearest"
    if(model=="nearest"):
        m=np.load(modelfile)
        labels=m[:,0]
        m=np.delete(m,0,1)
        with open(data,"r") as f:
            with open("output.txt","w") as of:
                count=0
                for line in f:
                    l=line.split()
                    sample=np.array(list(map(int,l[2:])))
                    dists=np.zeros(m.shape[0])
                    for i in range(m.shape[0]):
                        dists[i]=correlation(m[i],sample)
                    knn=labels[np.argpartition(dists,k)[0:k]]
                    res=scipy.stats.mode(knn)[0][0]
                    print(l[0],res,file=of)                
    elif(model=="tree"):
        with open(modelfile,'rb') as f:
            forest=pickle.load(f)
        with open(data,'r') as f:
            with open("output.txt","w") as of:
                total=0
                corrects=0
                for line in f:
                    l=line.split()
                    truth=int(l[1])
                    sample=list(map(int,l[2:]))
                    sample=np.array(sample)
                    ress=[]
                    for pairs,tree in forest:
                        newsample=(np.diff(sample[pairs])>0).T[0]
                        ress.append(tree_predict(tree,newsample))
                    res=scipy.stats.mode(ress)[0][0]
                    print(l[0],res,file=of)    
    elif(model=="nnet"):
        with open(modelfile,'rb') as f:
            net=pickle.load(f)
        w0=net[0]
        w1=net[1]
        with open(data,'r') as f:
            with open("output.txt","w") as of:
                for line in f:
                    l=line.split()
                    sample=list(map(int,l[2:]))
                    sample=np.array(sample)
                    y=np.argmax(softmax(expit(sample.dot(w0)).dot(w1)))
                    if(y==1):
                        y=90
                    elif(y==2):
                        y=180
                    elif(y==3):
                        y=270
                    print(l[0],y,file=of)
                

if(argv[1]=="train"):
    train(argv[2],argv[3],argv[4])
elif(argv[1]=="test"):
    test(argv[2],argv[3],argv[4])