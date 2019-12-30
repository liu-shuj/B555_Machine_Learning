import numpy as np
from numpy.linalg import inv
from scipy.special import expit

def TrainMLE(Phi:np.ndarray,t:np.ndarray):
    N=Phi.shape[0]
    n_feat=Phi.shape[1]
    count={0:0,1:0}
    sum_feat={0:np.zeros(n_feat),1:np.zeros(n_feat)}
    for i in range(0,N):
        count[t[i]]+=1
        sum_feat[t[i]]+=Phi[i]
    mu0=sum_feat[0]/count[0]
    mu1=sum_feat[1]/count[1]
    mu={0:mu0,1:mu1}
    sumT=count[0]+count[1]
    p0=count[0]/sumT
    p1=count[1]/sumT
    sumcov={0:0*np.eye(n_feat),1:0*np.eye(n_feat)}
    for i in range(0,N):
        sumcov[t[i]]+=(Phi[i]-mu[t[i]]).dot((Phi[i]-mu[t[i]]).T)
    S0=sumcov[0]/count[0]
    S1=sumcov[1]/count[1]
    S=p0*S0+p1*S1
    sigma=S+(1e-9)*np.eye(n_feat)
    w=inv(sigma).dot(mu0-mu1)
    w0=-0.5*mu0.T.dot(inv(sigma)).dot(mu0)+0.5*mu1.T.dot(inv(sigma)).dot(mu1)+np.log(p0/p1)
    return {'w':w,'w0':w0}

def Predict(model:dict,input:np.ndarray):
    w=model['w']
    w0=model['w0']
    a=w.T.dot(input)+w0
    P_0=expit(a)
    if(P_0>0.5 and P_0<=1):
        return 0
    elif(P_0<0.5 and P_0>=0):
        return 1
    elif(P_0==0.5):
        rand=np.random.randint(2)
        return (1 if rand==1 else 0)
    else:
        raise Exception("Invalid probability obtained")

