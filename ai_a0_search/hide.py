#!/usr/local/bin/python3
#
# hide.py : a simple friend-hider
#
# Submitted by : Shujun Liu(Username: liushuj) 
#
# Based on skeleton code by D. Crandall and Z. Kachwala, 2019
#
# The problem to be solved is this:
# Given a campus map, find a placement of F friends so that no two can find one another.
#

import sys

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().split("\n")]

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a friend to the board at the given position, and return a new board (doesn't change original)
def add_friend(board, row, col):
    return board[0:row] + [board[row][0:col] + ['F',] + board[row][col+1:]] + board[row+1:]

def draw_board(l_frs,IUB_map):
    for coord in l_frs:
        IUB_map=add_friend(IUB_map,coord[0],coord[1])
    return IUB_map

def gen_intervals(l):  
    # split ordered list of numbers into intervals:
    # e.g. [0 2 3 4 6 7] --> [[0] [2 3 4] [6 7]]
    i=0
    res=[]
    start=0
    while(i<len(l)):
        if(i+1==len(l) or l[i+1]-l[i]>1):
            res.append(l[start:i+1])
            start=i+1
        i+=1
    return res

       
def build_graph(d_flr_r,d_flr_c,c_mys,K):
    # Build a bipartite graph with left nodes all horizontal sections and right nodes all vertical sections
    n_int_h=0
    n_int_v=0
    for i in d_flr_r:
        d_flr_r[i]=gen_intervals(d_flr_r[i])
        n_int_h+=len(d_flr_r[i])
    for j in d_flr_c:
        d_flr_c[j]=gen_intervals(d_flr_c[j])
        n_int_v+=len(d_flr_c[j])
    boundK=min(n_int_h-1,n_int_v-1)  # fail when there're not enough intersections to use
    graph={}
    for r in d_flr_r:
        for i in d_flr_r[r]:
            graph[(r,tuple(i))]=[]
    for r in d_flr_r:
        for i in d_flr_r[r]:
            for c in i:
                for ci in d_flr_c[c]:
                    if r in ci and (r,c)!=c_mys:
                        graph[(r,tuple(i))].append((tuple(ci),c))
                        break
    return graph,boundK
    
def Search(graph,l_friends,s_inv_vs,K):
    if(K==0):
        return l_friends
    for u in graph:
        for v in graph[u]:
            if v in s_inv_vs:  # If conflict happens, backtrack immediately...
                if K>1:   # ...but not for the last K. small but speeds up!
                    return False
                else:
                    continue
            else:
                tmp=graph[u];graph[u]=[]
                result=Search(graph,l_friends+[(u[0],v[1])],s_inv_vs.union({v}),K-1)
                graph[u]=tmp
                if(result):
                    return result
    return False
            
# Main Function
if __name__ == "__main__":
    IUB_map=parse_map(sys.argv[1])
    if(IUB_map[-1]==[]):
        IUB_map.pop()
    # This is K, the number of friends
    K = int(sys.argv[2])
    if(K>len(IUB_map)*len(IUB_map[0])):
        print("None")
        exit(0)

    c_mys=()
    # dict of floors
    d_flr={x:[] for x in range(len(IUB_map))}
    d_flr_c={y:[] for y in range(len(IUB_map[0]))}
    for i in range(len(IUB_map)):
        for j in range(len(IUB_map[0])):
            if(IUB_map[i][j]=='.' or IUB_map[i][j]=="#"):
                d_flr[i].append(j)
                d_flr_c[j].append(i)
                if(IUB_map[i][j]=='#'):
                    c_mys=(i,j)

    graph,boundK=build_graph(d_flr,d_flr_c,c_mys,K)
    if(K>boundK):
        print("None");exit(0)
    solution=Search(graph,[],set(),K)
    if(solution!=False):
        print((printable_board(draw_board(solution,IUB_map))))
        exit(0)
    print("None")


