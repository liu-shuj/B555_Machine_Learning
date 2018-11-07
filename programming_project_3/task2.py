import numpy as np
from core.metrics import ClassErrorRate
from core import bayeslogistic
import matplotlib.pyplot as plt
import time

datasets=["A","usps"]
fractions = np.linspace(0.1, 1, 21)

sub=1
for dataset in datasets:
    print("Loading dataset {dataset}...".format(dataset=dataset))
    Phi=np.loadtxt("pp3data/{dataset}.csv".format(dataset=dataset),delimiter=",")
    t=np.loadtxt("pp3data/labels-{dataset}.csv".format(dataset=dataset),delimiter=",")
    errorsNewton=[[],[],[]]
    errorsGD=[[],[],[]]
    errorsSGD=[[],[],[]]
    timesNewton=[[],[],[]]
    timesGD=[[],[],[]]
    timesSGD=[[],[],[]]
    w=None
    #PhiTrain,tTrain,PhiTest,tTest=randomCVsplit(0.333,Phi,t)
    nTest=int(Phi.shape[0]/3)
    PhiTest=Phi[0:nTest]
    PhiTrain=Phi[nTest:]
    tTest=t[0:nTest]
    tTrain=t[nTest:]
    for j in range(0,3):
        spenttime = 0
        w=None
        for i in range(1,101):
            walltime=time.time()
            model=bayeslogistic.Train(PhiTrain,tTrain,method="Newton",iter=1,initw=w)
            spenttime=spenttime+time.time()-walltime
            w=model['w_MAP']
            prediction=list(map(lambda input:bayeslogistic.Predict(model,input),PhiTest))
            error=ClassErrorRate(prediction,tTest)
            timesNewton[j].append(spenttime)
            errorsNewton[j].append(error)
        spenttime = 0
        w=None
        for i in range(1,601):
            walltime=time.time()
            model=bayeslogistic.Train(PhiTrain,tTrain,method="GD",iter=10,initw=w)
            spenttime=spenttime+time.time()-walltime
            w=model['w_MAP']
            prediction=list(map(lambda input:bayeslogistic.Predict(model,input),PhiTest))
            error=ClassErrorRate(prediction,tTest)
            timesGD[j].append(spenttime)
            errorsGD[j].append(error)
        spenttime = 0
        w=None
        for i in range(1, 601):
            walltime = time.time()
            model = bayeslogistic.Train(PhiTrain, tTrain, method="SGD", iter=10, initw=w)
            spenttime = spenttime + time.time() - walltime
            w = model['w_MAP']
            prediction = list(map(lambda input: bayeslogistic.Predict(model, input), PhiTest))
            error = ClassErrorRate(prediction, tTest)
            timesSGD[j].append(spenttime)
            errorsSGD[j].append(error)

    tNewton=np.array(timesNewton).mean(0)
    eNewton=(1-np.array(errorsNewton)).mean(0)
    tGD=np.array(timesGD).mean(0)
    eGD=(1-np.array(errorsGD)).mean(0)
    tSGD=np.array(timesSGD).mean(0)
    eSGD=(1-np.array(errorsSGD)).mean(0)
    plt.subplot(2,1,sub)
    sub+=1
    plt.plot(tNewton,eNewton,color="#FF0000",label="Newton")
    plt.plot(tGD,eGD,color="#0000FF",label="Gradient")
    plt.plot(tSGD,eSGD,color="#00FF00",label="Stochastic Gradient")
    plt.title(dataset)

plt.legend(loc='lower right')
plt.show()
