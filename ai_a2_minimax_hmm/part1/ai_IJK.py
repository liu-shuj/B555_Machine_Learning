#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: Shujun Liu(liushuj)

Based on skeleton code by Abhilash Kuhikar, October 2019
"""

from logic_IJK import Game_IJK
import random
import copy
# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.

def evaluate(game: Game_IJK,player)->(int,int):
    up,low=0,0
    gamestate=game.state()
    if(gamestate=='C'):
        up=float("inf")
        low=float("-inf")
        return float("inf")
    elif(gamestate=='c'):
        return float("-inf")
    elif(gamestate=='Tie'):
        return 0
    adjscore=0
    board=game.getGame()
    for row in board:
        for e in row:
            if(e!=' '):
                if(e>='a'):
                    low+=(2**(ord(e)-ord('a')+1)-1)
                else:
                    up+=(2**(ord(e)-ord('A')+1)-1)
    for i in range(6):
        for j in range(6):
            if(j+1<6 and abs(ord(board[i][j+1])-ord(board[i][j]))==32):
                adjscore+=(2**(ord(board[i][j+1])-ord('a')+2)-1)
            elif(i+1<6 and abs(ord(board[i+1][j])-ord(board[i][j]))==32):
                adjscore+=(2**(ord(board[i+1][j])-ord('a')+2)-1)
    return up-low+(adjscore if game.getCurrentPlayer()==player else -adjscore)
    
def MAX_Value(game:Game_IJK,alpha:int,beta:int,depth:int,player:str)->int:
    curalpha=alpha
    if(depth==0):
        upscore=evaluate(game,player)
        return upscore if player=='+' else -upscore
    gamestate=game.state()
    if(gamestate=='C'):
        return float("inf") if player=='+' else float("-inf")
    elif(gamestate=='c'):
        return float("-inf") if player=='+' else float("inf")
    elif(gamestate=='Tie'):
        return 0
    w=copy.deepcopy(game)
    w=w.makeMove('U')
    s=copy.deepcopy(game)
    s=w.makeMove('D')
    a=copy.deepcopy(game)
    a=w.makeMove('L')
    d=copy.deepcopy(game)
    d=w.makeMove('R')
    for g in [w,s,a,d]:
        curalpha=max(curalpha,MIN_Value(g,curalpha,beta,depth-1,player))
        if(curalpha>=beta):
            return curalpha
    return curalpha
        
def MIN_Value(game:Game_IJK,alpha:int,beta:int,depth:int,player:str)->int:
    curbeta=beta
    if(depth==0):
        upscore=evaluate(game,player)
        return upscore if player=='+' else -upscore
    gamestate=game.state()
    if(gamestate=='C'):
        return float("inf") if player=='+' else float("-inf")
    elif(gamestate=='c'):
        return float("-inf") if player=='+' else float("inf")
    elif(gamestate=='Tie'):
        return 0
    w=copy.deepcopy(game)
    w=w.makeMove('U')
    s=copy.deepcopy(game)
    s=w.makeMove('D')
    a=copy.deepcopy(game)
    a=w.makeMove('L')
    d=copy.deepcopy(game)
    d=w.makeMove('R')
    for g in [w,s,a,d]:
        curbeta=min(curbeta,MAX_Value(g,alpha,curbeta,depth-1,player))
        if(alpha>=curbeta):
            return curbeta
    return curbeta
    
def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''

    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()    

    # You'll want to put in your fancy AI code here. For right now this just 
    # returns a random move.
    if(deterministic):
        depth=6
    else:
        depth=0
    mins={}
    w=copy.deepcopy(game)
    w=w.makeMove('U')
    s=copy.deepcopy(game)
    s=w.makeMove('D')
    a=copy.deepcopy(game)
    a=w.makeMove('L')
    d=copy.deepcopy(game)
    d=w.makeMove('R')
    mins['U']=MIN_Value(w,float("-inf"),float("inf"),depth,player)
    mins['D']=MIN_Value(s,float("-inf"),float("inf"),depth,player)
    mins['L']=MIN_Value(a,float("-inf"),float("inf"),depth,player)
    mins['R']=MIN_Value(d,float("-inf"),float("inf"),depth,player)
    move=max(mins,key=lambda k:mins[k])
    for i in range(6):
        for j in range(6):
            if(j+1<6 and abs(ord(board[i][j+1])-ord(board[i][j]))==32):
                move='R'
            elif(i+1<6 and abs(ord(board[i+1][j])-ord(board[i][j]))==32):
                move='D'
    yield move
