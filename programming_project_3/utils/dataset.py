import numpy as np
from typing import Union,Tuple

def randsubset(fraction:float,data:np.ndarray,labels:np.ndarray=None)->Union[Tuple[np.ndarray,np.ndarray],np.ndarray]:
    N=data.shape[0]
    size=int(N*fraction)
    samples=np.random.choice(N,size,replace=False)
    subset=data[samples]
    if labels is not None:
        subl=labels[samples]
        return subset,subl
    else:
        return subset

def randomCVsplit(vfraction:float,data:np.ndarray,labels:np.ndarray=None)->Union[Tuple[np.ndarray,np.ndarray,np.ndarray,np.ndarray],Tuple[np.ndarray,np.ndarray]]:
    N=data.shape[0]
    vsize=int(N*vfraction)  # size of Validation set
    perm = np.random.permutation(range(0, N))
    itest=perm[0:vsize]
    itrain=perm[vsize:]
    trainset=data[itrain]
    testset=data[itest]
    if labels is not None:
        trainl=labels[itrain]
        testl=labels[itest]
        return trainset,trainl,testset,testl
    else:
        return trainset,testset

