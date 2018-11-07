import numpy as np
from utils.dataset import randsubset
from typing import Callable,Union

def CalcMSE(x:np.ndarray,y:np.ndarray)->np.ndarray:
    return ((x-y)**2).mean(0)

def ClassErrorRate(x:np.ndarray,y:np.ndarray)->np.ndarray:
    return (x!=y).mean(0)

def LearningCurve(TrainFunc:Callable[[np.ndarray,np.ndarray],Union[np.ndarray,list]],
                  TestFunc:Callable[[np.ndarray,np.ndarray],Union[np.ndarray,list]],
                  fractions:np.ndarray,
                  mTrain:np.ndarray,lTrain:np.ndarray,
                  mTest:np.ndarray,lTest:np.ndarray,method="regression")->(list,list):
    N=mTrain.shape[0]  # total count of samples
    if(method=="regression"):
        MSE=[]
        for fraction in fractions:
            subset,subT=randsubset(fraction,mTrain,lTrain)
            model = TrainFunc(subset,subT)
            pTest = TestFunc(model,mTest)
            MSE.append(CalcMSE(pTest,lTest))  # MSE=∑((t_p-t)**2)/N
        return fractions,MSE
    elif(method=="classification"):
        Error=[]
        for fraction in fractions:
            subset,subT=randsubset(fraction,mTrain,lTrain)
            model = TrainFunc(subset,subT)
            pTest = TestFunc(model,mTest)
            Error.append(ClassErrorRate(pTest,lTest))
        return fractions,Error
    else:
        raise Exception("Method not supported")