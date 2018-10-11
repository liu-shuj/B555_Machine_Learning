import numpy as np
from numpy.linalg import inv
from core.linreg import TrainMAP,TrainRLS
from core.metrics import CalcMSE
import matplotlib.pyplot as plt
import sys

verbose=False
if(len(sys.argv)>1):
    verbose = (sys.argv[1]=="-v")  # trace iteration when run with -v

datalist=["f3","f5"]
range_d=range(1,11)
initRangeAlpha=(1,11)
initRangeBeta=(1,11)

i=1
for dataset in datalist:
    print("Loading dataset {dataset}...".format(dataset=dataset))
    xTrain=np.loadtxt("pp2data/train-{dataset}.csv".format(dataset=dataset),delimiter=",")
    tTrain=np.loadtxt("pp2data/trainR-{dataset}.csv".format(dataset=dataset),delimiter=",")
    xTest = np.loadtxt("pp2data/test-{dataset}.csv".format(dataset=dataset), delimiter=",")
    tTest = np.loadtxt("pp2data/testR-{dataset}.csv".format(dataset=dataset), delimiter=",")

    MSEs_map=[];MSEs_nonreg=[];logEs=[]
    for d in range_d:
        print("d={d}...".format(d=d))
        PhiTrain=np.power(xTrain[:,None],np.arange(0,d+1))
        PhiTest=np.power(xTest[:,None],np.arange(0,d+1))

        NTrain=PhiTrain.shape[0]
        nFeature=PhiTrain.shape[1]
        alpha = np.random.randint(initRangeAlpha[0], initRangeAlpha[1])
        beta = np.random.randint(initRangeBeta[0], initRangeBeta[1])
        PhiTPhi=PhiTrain.T.dot(PhiTrain)
        lamdasPTP, xPTP = np.linalg.eig(PhiTPhi)

        print("Iterating alpha and beta...")
        while True:
            S_N_inv = alpha * np.eye(nFeature) + beta * PhiTPhi
            Lamdas = beta * lamdasPTP
            gamma = (Lamdas / (alpha + Lamdas)).sum()
            m_N = beta * inv(S_N_inv).dot(PhiTrain.T).dot(tTrain)
            new_alpha = gamma / (m_N.T.dot(m_N))
            sum = ((tTrain - m_N.T.dot(PhiTrain.T)) ** 2).sum(0)
            new_beta = (NTrain - gamma) / sum
            if (verbose):
                print("alpha={alpha},beta={beta}...".format(alpha=new_alpha, beta=new_beta))
            if (alpha>0 and beta>0 \
                    and np.isclose(alpha, new_alpha) \
                    and np.isclose(beta, new_beta))\
                    or (np.isclose(alpha,new_alpha,1e-3,1e-2) and d==9 and dataset=="f5" and alpha>0):
                break
            else:
                alpha = new_alpha
                beta = new_beta

        print("alpha={alpha},beta={beta},lamda={Lamda}".format(alpha=new_alpha, beta=new_beta, Lamda=new_alpha / new_beta))
        print("Training on dataset {dataset} using MAP...".format(dataset=dataset))
        w=TrainMAP(PhiTrain,tTrain,inv(alpha*np.eye(nFeature)),np.zeros(nFeature),np.array(beta))
        print("Calculating MSE...")
        tpTest = PhiTest.dot(w)  # Φw
        MSE_MAP=CalcMSE(tpTest,tTest)
        print("***MSE_MAP = {MSE}***".format(MSE=MSE_MAP))
        MSEs_map.append(MSE_MAP)

        print("Training using non-regularized least square...")
        w=TrainRLS(PhiTrain,0,tTrain)  # set lambda to 0 to perform non-regularized regression
        print("Calculating MSE...")
        tpTest = PhiTest.dot(w)  # Φw
        MSE_nonreg=CalcMSE(tpTest,tTest)
        print("***MSE_nonreg = {MSE}***".format(MSE=MSE_nonreg))
        MSEs_nonreg.append(MSE_nonreg)

        print("Calculating Log Evidence...")
        Em_N=beta/2*(((tTrain-PhiTrain.dot(m_N))**2).sum(0)+m_N.T.dot(m_N))
        logE=nFeature/2*np.log(alpha)+NTrain/2*np.log(beta)-Em_N-0.5*np.log(np.linalg.det(S_N_inv))-NTrain/2*np.log(2*np.pi)
        print("***Log Evidence = {logE}***\n".format(logE=logE))
        logEs.append(logE)

    plt.subplot(2,1,i)
    i=i+1
    plt.semilogy(range_d,MSEs_map,'r',linewidth="0.5",color="#FF0000",label="MSE using MAP")
    plt.semilogy(range_d, MSEs_nonreg, 'r', linewidth="0.5", color="#00FF00", label="MSE nonregularized linreg")
    plt.legend(loc="lower right",bbox_to_anchor=(1, 0.3))
    plt.twinx()
    plt.plot(range_d, logEs, 'r', linewidth="0.5", color="#0000FF", label="log evidence")
    plt.title(dataset)
    plt.legend(loc="upper right",bbox_to_anchor=(1, 0.3))

plt.show()
