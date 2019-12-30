#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: Shujun Liu (Username: liushuj) 
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import sys

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
MOVEL = {"A":(2,1),"B":(2,-1),"C":(-2,1),"D":(-2,-1),"E":(1,2),"F":(1,-2),"G":(-1,2),"H":(-1,-2)}
MOVE=MOVES

def rowcol2ind(row, col):
    return row*4 + col

def ind2rowcol(ind):
    return (int(ind/4), ind % 4)

def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3

def swap_ind(t, ind1, ind2):
    return t[0:ind1] + (t[ind2],) + t[ind1+1:ind2] + (t[ind1],) + t[ind2+1:]

def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1,col1), rowcol2ind(row2,col2)))))

def printable_board(row):
    return [ '%3d %3d %3d %3d'  % (row[j:(j+4)]) for j in range(0, 16, 4) ]

# return a list of possible successor states
def successorS(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, empty_row+i, empty_col+j), c) \
             for (c, (i, j)) in MOVE.items() if valid_index(empty_row+i, empty_col+j) ]

def successorC(state):
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    return [ (swap_tiles(state, empty_row, empty_col, (empty_row+i)%4, (empty_col+j)%4), c) \
             for (c, (i, j)) in MOVE.items()]
             
def Manhattan(state):
    res=0
    for i in range(len(state)):
        if(state[i]!=0):
            curr_rc=ind2rowcol(i)
            goal_rc=ind2rowcol(state[i]-1)
            res+=(abs(curr_rc[0]-goal_rc[0])+abs(curr_rc[1]-goal_rc[1]))
    return res
    
def Nmisplaced(state):
    res=0
    for i in range(len(state)):
        if(state[i]!=0):
            res+=(1 if state[i]!=i+1 else 0)
    return res

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1]==0

def solvable(state):
    inv=0
    l=list(state)
    evenodd=1 if ind2rowcol(l.index(0))[0]%2==0 else 0
    l.remove(0)
    
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            if(l[i]>l[j]):
                inv+=1
    return (inv%2==evenodd)

# test cases
if __name__ == "__main__":
    if(len(sys.argv) != 3):
        raise(Exception("Error: expected 2 arguments"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if(sys.argv[2]=="original"):
        MOVE=MOVES
        successors=successorS
        h=lambda x:Manhattan(x)
    elif(sys.argv[2]=="circular"):
        MOVE=MOVES
        successors=successorC
        h=Nmisplaced
    elif(sys.argv[2]=="luddy"):
        MOVE=MOVEL
        successors=successorS
        h=lambda s:Manhattan(s)/3
    else:
        print("Mode not supported.")
        exit(0)
            
    if len(start_state) != 16:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")     
    if ((sys.argv[2]=="original") and (not solvable(start_state))):
        print("Inf")
        exit(0)
    g={}
    hq=PriorityQueue()
    hq.put_nowait((h(start_state),0,"",tuple(start_state)))
    FVAL=0;GVAL=1;PATH=2;STAT=3
    while not hq.empty():
        cur=hq.get_nowait()
        if(is_goal(cur[STAT])):
            print("Solution found in " + str(cur[GVAL]) + " moves:" + "\n" + cur[PATH])
            exit(0) 
        for (succ,move) in successors(cur[STAT]):
            new_g=cur[GVAL]+1
            if((succ not in g) or (new_g<g[succ])):
                g[succ]=new_g
                hq.put_nowait((new_g+h(succ),new_g,cur[PATH]+move,succ))
    print("Inf")
    

