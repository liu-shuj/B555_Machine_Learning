import numpy as np
from utils.dataset import randomCVsplit
from core.metrics import LearningCurve
from core import bayeslogistic,bingenerative
import matplotlib.pyplot as plt

datasets=["A","B","usps"]
fractions = np.linspace(0.1, 1, 21)

sub=1
for dataset in datasets:
    print("Loading dataset {dataset}...".format(dataset=dataset))
    Phi=np.loadtxt("pp3data/{dataset}.csv".format(dataset=dataset),delimiter=",")
    t=np.loadtxt("pp3data/labels-{dataset}.csv".format(dataset=dataset),delimiter=",")
    errorsGen=[]
    errorsLR=[]
    for i in range(0,30):
        PhiTrain,tTrain,PhiTest,tTest=randomCVsplit(0.333,Phi,t)
        TrainFunc=lambda Phi,t:bingenerative.TrainMLE(Phi,t)
        TestFunc=lambda model,inputM:list(map(lambda input:bingenerative.Predict(model,input),inputM))
        errorsGen.append(LearningCurve(TrainFunc,TestFunc,fractions,PhiTrain,tTrain,PhiTest,tTest,method="classification")[1])
    for i in range(0,30):
        PhiTrain,tTrain,PhiTest,tTest=randomCVsplit(0.333,Phi,t)
        TrainFunc=lambda Phi,t:bayeslogistic.Train(Phi,t,method="Newton",iter=100)
        TestFunc=lambda model,inputM:list(map(lambda input:bayeslogistic.Predict(model,input),inputM))
        errorsLR.append(LearningCurve(TrainFunc,TestFunc,fractions,PhiTrain,tTrain,PhiTest,tTest,method="classification")[1])
    meGen=1-(np.array(errorsGen).mean(0))
    stdGen=np.array(errorsGen).std(0)
    meLR=1-(np.array(errorsLR).mean(0))
    stdLR=np.array(errorsLR).std(0)
    plt.subplot(2,2,sub)
    sub+=1
    plt.errorbar(fractions,meGen,yerr=stdGen,color="#FF0000",label="Generative")
    plt.errorbar(fractions, meLR, yerr=stdLR,color="#0000FF",label="Logistic")
    plt.title(dataset)

plt.legend(loc='lower right')
plt.show()
