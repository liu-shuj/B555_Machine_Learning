import numpy as np
from numpy.linalg import inv

def TrainRLS(Phi:np.ndarray,Lamda:float,t:np.ndarray)->np.ndarray:
    n=Phi.shape[1]  # count of features
    I=np.eye(n)
    w=inv((Lamda*I+Phi.T.dot(Phi))).dot(Phi.T).dot(t)
    return w

def TrainMAP(Phi:np.ndarray,t:np.ndarray,S_0:np.ndarray,m_0:np.ndarray,Beta:np.ndarray)->np.ndarray:
    S_N_inv=inv(S_0)+Beta.dot(Phi.T).dot(Phi)
    m_N=inv(S_N_inv).dot(inv(S_0).dot(m_0)+Beta.dot(Phi.T).dot(t))
    w=m_N
    return w

def Predict(w:np.ndarray,input:np.ndarray):
    return input.dot(w)