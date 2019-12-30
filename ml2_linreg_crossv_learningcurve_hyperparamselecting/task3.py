import numpy as np
from numpy.linalg import inv
from core.linreg import TrainMAP
from core.metrics import CalcMSE
import sys

verbose=False
if(len(sys.argv)>1):
    verbose = (sys.argv[1]=="-v")  # trace iteration when run with -v

datalist=["100-10","100-100","1000-100","crime","wine"]
initRangeAlpha=(1,11)
initRangeBeta=(1,11)

for dataset in datalist:
    print("Loading dataset {dataset}...".format(dataset=dataset))
    PhiTrain=np.loadtxt("pp2data/train-{dataset}.csv".format(dataset=dataset),delimiter=",")
    tTrain=np.loadtxt("pp2data/trainR-{dataset}.csv".format(dataset=dataset),delimiter=",")
    PhiTest = np.loadtxt("pp2data/test-{dataset}.csv".format(dataset=dataset), delimiter=",")
    tTest = np.loadtxt("pp2data/testR-{dataset}.csv".format(dataset=dataset), delimiter=",")

    print("Initializing...")
    NTrain=PhiTrain.shape[0]
    nFeature=PhiTrain.shape[1]
    alpha = np.random.randint(initRangeAlpha[0], initRangeAlpha[1])
    beta = np.random.randint(initRangeBeta[0], initRangeBeta[1])
    PhiTPhi=PhiTrain.T.dot(PhiTrain)
    lamdasPTP, xPTP = np.linalg.eig(PhiTPhi)

    print("Iterating alpha and beta...")
    while True:
        S_N_inv = alpha * np.eye(nFeature) + beta * PhiTPhi
        Lamdas=beta*lamdasPTP
        gamma=(Lamdas/(alpha+Lamdas)).sum()
        m_N=beta*inv(S_N_inv).dot(PhiTrain.T).dot(tTrain)
        new_alpha=gamma/(m_N.T.dot(m_N))
        sum=((tTrain-m_N.T.dot(PhiTrain.T))**2).sum(0)
        new_beta=(NTrain-gamma)/sum
        if(verbose):
            print("alpha={alpha},beta={beta}...".format(alpha=new_alpha, beta=new_beta))
        if np.isclose(alpha,new_alpha) and np.isclose(beta,new_beta):
            break
        else:
            alpha=new_alpha
            beta=new_beta

    print("alpha={alpha},beta={beta},lamda={Lamda}".format(alpha=new_alpha, beta=new_beta,Lamda=new_alpha/new_beta))
    print("Training on dataset {dataset} using MAP...".format(dataset=dataset))
    w=TrainMAP(PhiTrain,tTrain,inv(alpha*np.eye(nFeature)),np.zeros(nFeature),np.array(beta))
    print("Calculating MSE...")
    tpTest = PhiTest.dot(w)  # Φw
    MSE=CalcMSE(tpTest,tTest) # MSE=∑((t_p-t)**2)/N
    print("MSE={MSE}\n".format(MSE=MSE))
