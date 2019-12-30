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
