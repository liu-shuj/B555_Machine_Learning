import numpy as np
from utils.dataset import randomCVsplit
from core.metrics import LearningCurve
from core import bayeslogistic,bingenerative
import matplotlib.pyplot as plt

datasets=["A","B","usps"]
fractions = np.linspace(0.1, 1, 21)
learning_rates=[5*1e-3,1e-3,5*1e-4,1e-4]
colors=["#FF0000","#00FF00","#0000FF","#0F0F0F"]

sub=1
for dataset in datasets:
    plt.subplot(2,2,sub)
    sub+=1
    print("Loading dataset {dataset}...".format(dataset=dataset))
    Phi=np.loadtxt("pp3data/{dataset}.csv".format(dataset=dataset),delimiter=",")
    t=np.loadtxt("pp3data/labels-{dataset}.csv".format(dataset=dataset),delimiter=",")
    for learning_rate in learning_rates:
        errors=[]
        for i in range(0,30):
            PhiTrain,tTrain,PhiTest,tTest=randomCVsplit(0.333,Phi,t)
            TrainFunc=lambda Phi,t:bayeslogistic.Train(Phi,t,method="SGD",iter=6000,eta=learning_rate)
            TestFunc=lambda model,inputM:list(map(lambda input:bayeslogistic.Predict(model,input),inputM))
            errors.append(LearningCurve(TrainFunc,TestFunc,fractions,PhiTrain,tTrain,PhiTest,tTest,method="classification")[1])
        errors=np.array(errors).mean(0)
        plt.plot(fractions, 1-errors, color=colors[learning_rates.index(learning_rate)], label=learning_rate)
    plt.title(dataset)

plt.legend(loc='lower right')
plt.show()
