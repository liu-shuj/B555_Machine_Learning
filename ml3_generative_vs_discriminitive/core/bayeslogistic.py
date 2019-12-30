import numpy as np
from numpy.linalg import inv
from scipy.special import expit

def Train(PhiOrig:np.ndarray,t:np.ndarray,method:str,initw=None,alpha=0.1,eta=1e-3,precision=1e-3,iter=6000):
    N=PhiOrig.shape[0]
    ones=np.ones(N)
    Phi=np.c_[ones,PhiOrig]
    n_feat=Phi.shape[1]
    if initw is None:
        w = np.zeros(n_feat)
    else:
        w=initw
    w_new = np.inf * np.ones(n_feat)
    n_iter = 0
    y = np.zeros(N)
    if(method=="Newton"):
        while True:
            R=np.eye(N)
            for i in range(0,N):
                y[i]=expit(w.T.dot(Phi[i]))
                R[i][i]=y[i]*(1-y[i])
            w_new=w-(inv(alpha*np.eye(n_feat)+Phi.T.dot(R).dot(Phi)).dot(Phi.T.dot(y-t)+alpha*w))
            n_iter=n_iter+1
            if (((np.sum((w_new-w)**2)/np.sum(w**2))<precision) or (n_iter>=iter)):
                w=w_new
                break
            w=w_new
    elif(method=="GD"):
        while True:
            for i in range(0,N):
                y[i]=expit(w.T.dot(Phi[i]))
            w_new=w-eta*(Phi.T.dot(y-t)+alpha*w)
            n_iter=n_iter+1
            if (((np.sum((w_new-w)**2)/np.sum(w**2))<precision) or (n_iter>=iter)):
                w=w_new
                break
            w=w_new
    elif(method=="SGD"):
        flag=0
        while True:
            perm=np.random.permutation(range(0,N))
            for index in perm:
                row=Phi[index]
                t_i=t[index]
                y_i=expit(w.T.dot(row))
                w_new=w-eta*((y_i-t_i)*row+alpha*w)
                n_iter = n_iter + 1
                if (((np.sum((w_new-w)**2)/np.sum(w**2))<precision) or (n_iter>=iter)):
                    w=w_new
                    flag=1
                    break
                w=w_new
            if(flag):
                break
    else:
        raise Exception("Method not supported")

    for i in range(0, N):
        y[i] = expit(w.T.dot(Phi[i]))
    sum=0
    for i in range(0,N):
        sum=sum+y[i]*(1-y[i])*Phi[i].dot(Phi[i].T)
    S_N=inv(inv(alpha*np.eye(n_feat))+sum)
    return {'w_MAP':w,'S_N':S_N}

def Predict(model:dict,input:np.ndarray):
    w_MAP=model['w_MAP']
    S_N=model['S_N']
    phi=np.r_[1,input]
    mu=w_MAP.T.dot(phi)
    sigma2=phi.T.dot(S_N).dot(phi)
    P_1=expit(((1+np.pi*sigma2/8)**(-0.5))*mu)
    if(P_1>0.5 and P_1<=1):
        return 1
    elif(P_1<0.5 and P_1>=0):
        return 0
    elif(P_1==0.5):
        rand=np.random.randint(2)
        return (1 if rand==1 else 0)
    else:
        raise Exception("Invalid probability obtained")
