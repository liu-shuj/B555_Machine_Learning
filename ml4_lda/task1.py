import os
from core.LatentDirichletAllocation import ExtractLDA

n_topics=20
filelist=map(str,range(1,201))
data_path="pp4data/20newsgroups"
top=5

doclist=[]
for filename in filelist:
    file_path = os.path.join(data_path,filename)
    if os.path.isfile(file_path):
        with open(file_path,'r') as f:
            doclist.append(f.read().split())

dl,z,C_d,C_t=ExtractLDA(n_topics,doclist)

with open("topicwords.csv",'w') as fout:
    for i in range(0,n_topics):
        l=C_t[i].tolist()
        d={l[i]:i for i in range(0,len(l))}
        sortedl=sorted(d,reverse=True)
        for j in range(0, top):
            fout.write(dl[d[sortedl[j]]])
            fout.write(" ")
        fout.write("\n")
