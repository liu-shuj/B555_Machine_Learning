import os
import numpy as np
from core.LatentDirichletAllocation import ExtractLDA,BagOfWords
from core import bayeslogistic
from core.metrics import LearningCurve
from utils.dataset import randomCVsplit
import matplotlib.pyplot as plt

n_topics=20
filelist=map(str,range(1,201))
data_path="pp4data/20newsgroups"
fractions=np.linspace(0.1, 1, 21)
repeat_times=30

label=np.loadtxt(os.path.join(data_path,"index.csv"),delimiter=",")[:,1]

doclist=[]
for filename in filelist:
    file_path = os.path.join(data_path,filename)
    if os.path.isfile(file_path):
        with open(file_path,'r') as f:
            doclist.append(f.read().split())

dl,z,C_d,C_t=ExtractLDA(n_topics,doclist)

l_d_bow=[BagOfWords(doc,dictionary=dl) for doc in doclist]
m_bow=[]
for d_bow in l_d_bow:
    v_bow=[]
    for key in dl:
        v_bow.append(d_bow[key])
    m_bow.append(v_bow)
m_bow=np.array(m_bow)

TrainFunc = lambda data, label: bayeslogistic.Train(data, label, "Newton", alpha=0.01, iter=100, precision=1e-5)
TestFunc = lambda model, inputM: list(map(lambda input: bayeslogistic.Predict(model, input), inputM))
ErrorLDA=[]
ErrorBOW=[]
for i in range(0,repeat_times):
    trainsetLDA,trainl,testsetLDA,testl=randomCVsplit(0.333,C_d,label)
    trainsetBOW,trainlBOW,testsetBOW,testlBOW=randomCVsplit(0.333,m_bow,label)
    ErrorLDA.append(LearningCurve(TrainFunc,TestFunc,fractions,trainsetLDA,trainl,testsetLDA,testl,method="classification")[1])
    ErrorBOW.append(LearningCurve(TrainFunc,TestFunc,fractions,trainsetBOW,trainlBOW,testsetBOW,testlBOW,method="classification")[1])

accLDA=1-np.array(ErrorLDA).mean(0)
accBOW=1-np.array(ErrorBOW).mean(0)
stdLDA=np.array(accLDA).std(0)
stdBOW=np.array(accBOW).std(0)

plt.errorbar(fractions,accLDA,yerr=stdLDA,color="#FF0000",label="LDA")
plt.errorbar(fractions,accBOW,yerr=stdBOW,color="#0000FF",label="Bag of Words")
plt.legend(loc='best')
plt.show()