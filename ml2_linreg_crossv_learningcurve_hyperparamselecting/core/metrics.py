import numpy as np
from utils.dataset import randsubset
from typing import Tuple,Callable

def CalcMSE(x:np.ndarray,y:np.ndarray)->np.ndarray:
    return ((x-y)**2).mean(0)

def LearningCurve(TrainFunc:Callable[[np.ndarray,np.ndarray],np.ndarray],
                  TestFunc:Callable[[np.ndarray,np.ndarray],np.ndarray],
                  fractions:np.ndarray,
                  mTrain:np.ndarray,lTrain:np.ndarray,
                  mTest:np.ndarray,lTest:np.ndarray)->(list,list):
    N=mTrain.shape[0]  # total count of samples
    MSE=[]
    for fraction in fractions:
        subset,subT=randsubset(fraction,mTrain,lTrain)
        param=TrainFunc(subset,subT)
        pTest = TestFunc(mTest,param)
        MSE.append(CalcMSE(pTest,lTest))  # MSE=∑((t_p-t)**2)/N
    return fractions,MSE