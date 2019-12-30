import numpy as np
from core.linreg import TrainRLS
import matplotlib.pyplot as plt
from core.metrics import CalcMSE

datalist=["100-10","100-100","1000-100","crime","wine"]
i=1

for dataset in datalist:
    print("Loading dataset {dataset}...".format(dataset=dataset))
    PhiTrain=np.loadtxt("pp2data/train-{dataset}.csv".format(dataset=dataset),delimiter=",")
    tTrain=np.loadtxt("pp2data/trainR-{dataset}.csv".format(dataset=dataset),delimiter=",")
    PhiTest = np.loadtxt("pp2data/test-{dataset}.csv".format(dataset=dataset), delimiter=",")
    tTest = np.loadtxt("pp2data/testR-{dataset}.csv".format(dataset=dataset), delimiter=",")
    l=[];MSETrain=[];MSETest=[]
    print("Iterating Lamda...")
    for Lamda in range(0,151):
        w=TrainRLS(PhiTrain,Lamda,tTrain)
        tpTrain=PhiTrain.dot(w)
        tpTest=PhiTest.dot(w)  # Φw
        MSETrain.append(CalcMSE(tpTrain,tTrain))
        MSETest.append(CalcMSE(tpTest,tTest)) # MSE=∑((t_p-t)**2)/N
        l.append(Lamda)
    print("Minimum MSE of training set is {min} when Lamda={lamda}"
          .format(min=min(MSETrain),lamda=MSETrain.index(min(MSETrain))))
    print("Minimum MSE of test set is {min} when Lamda={lamda}"
          .format(min=min(MSETest),lamda=MSETest.index(min(MSETest))))
    print("Plotting...")
    plt.subplot(2,3,i)
    i=i+1
    plt.plot(l,MSETrain,'r',linewidth="0.5",color="#FF0000",label="training")
    plt.plot(l,MSETest,'r',linewidth="0.5",color="#0000FF",label="test")
    plt.title(dataset)

plt.subplots_adjust(wspace=0.3,hspace=0.25)
plt.legend(loc='lower right')
plt.show()