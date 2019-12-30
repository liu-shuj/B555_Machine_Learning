#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: Shujun Liu (Username: liushuj) 
#
#
import sys
sys.setrecursionlimit(1000000)
name=[]
skill=[]
cost=[]
skill_out=[]
cost_out=[]
store=[]
def load_people(filename):
    with open(filename, "r") as file:
        for line in file:
            l = line.rstrip().split()
            name.append(l[0])
            skill.append(round(float(l[1])*100000));skill_out.append(float(l[1]))
            cost.append(round(float(l[2])*100000));cost_out.append(float(l[2]))
            store.append({})

def solve(i,b):
    if(i==-1):
        return 0
    if(b in store[i]):
        return store[i][b]
    opt1=solve(i-1,b)
    if(b-cost[i]>=0): # only try to hire when we can afford
        opt2=solve(i-1,b-cost[i])+skill[i]
    else:
        opt2=0
    ans=max(opt1,opt2)
    store[i][b]=ans
    return ans

if __name__ == "__main__":

    if(len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')
    chosen=[]
    budget = int(100000*float(sys.argv[2]))
    load_people(sys.argv[1])
    i=len(name)-1;b=budget
    res=solve(i,b)
    while True:
        if(i==0):
            if(b in store[0]):
                if(store[0][b]==res):
                    chosen.append(0) 
            break
        if(b in store[i-1]):
            if(store[i-1][b]==store[i][b]):
                i=i-1
                continue
        chosen.append(i)
        b=b-cost[i]
        res=res-skill[i]
        if(res==0):
            break
        i=i-1
    print("Found a group with %d people costing %f with total skill %f" % \
               ( len(chosen), sum(cost_out[j] for j in chosen), sum(skill_out[j] for j in chosen)))

    for j in chosen:
        print("{:} {:f}".format(name[j],1))

