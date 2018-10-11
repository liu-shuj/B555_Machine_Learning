import numpy as np
from core.metrics import LearningCurve
from core.linreg import TrainRLS
import matplotlib.pyplot as plt

dataset="1000-100"
Lamdas=[1,27,150]
fractions = np.linspace(0.1, 0.8, 36)  # size of random subsets as fractions of the data set
Colors={Lamdas[0]:"#FF0000",Lamdas[1]:"#00FF00",Lamdas[2]:"#0000FF"}

print("Loading dataset {dataset}...".format(dataset=dataset))
PhiTrain=np.loadtxt("pp2data/train-{dataset}.csv".format(dataset=dataset),delimiter=",")
tTrain=np.loadtxt("pp2data/trainR-{dataset}.csv".format(dataset=dataset),delimiter=",")
PhiTest = np.loadtxt("pp2data/test-{dataset}.csv".format(dataset=dataset), delimiter=",")
tTest = np.loadtxt("pp2data/testR-{dataset}.csv".format(dataset=dataset), delimiter=",")

for Lamda in Lamdas:
    print("Plotting learning curve when Lamda={Lamda}...".format(Lamda=Lamda))
    fractions,MSEList=LearningCurve(lambda phi,t:TrainRLS(phi,Lamda,t),lambda phi,w:phi.dot(w),
                                    fractions,PhiTrain,tTrain,PhiTest,tTest)
    plt.plot(fractions,MSEList,'r',linewidth="0.5",color=Colors[Lamda],label="Lamda={Lamda}".format(Lamda=Lamda))

plt.legend(loc='upper right')
plt.show()
