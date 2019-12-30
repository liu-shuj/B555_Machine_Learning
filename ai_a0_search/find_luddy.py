#!/usr/local/bin/python3
#
# find_luddy.py : a simple maze solver
#
# Submitted by : Shujun Liu (Username:liushuj) 
#
# Based on skeleton code by Z. Kachwala, 2019
#

import sys
import json

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().split("\n")]

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
	return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
	moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

	# Return only moves that are within the board and legal (i.e. on the sidewalk ".")
	return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]
# Perform search on the map
def search1(IUB_map,threshold,r_L,c_L):
	f_min=float("inf")
	path=[]
	fringe=[(-1,you_loc,0)]
	while fringe:
		(parent,curr_move, curr_dist)=fringe.pop()
		path.append(curr_move)
		flag=False # whether at least one new node is pushed to the fringe
		for move in moves(IUB_map, *curr_move):
			if IUB_map[move[0]][move[1]]=="@":
				path.append(move)
				return ((curr_dist+1,path),f_min)
			else:
				if(move in path):
					continue
				new_h=abs(move[0]-r_L)+abs(move[1]-c_L)
				new_f=curr_dist+1+new_h
				if(new_f<=threshold):
					fringe.append((curr_move,move, curr_dist + 1))
					flag=True
				else:
					if(new_f<f_min):
						f_min=new_f
		if not flag:
			while fringe==[] or fringe[-1][0]!=path[-1]:
				path.pop() # cut off the whole dead end path
				if(path==[]):
					break
	return (False,f_min)

# Convert path in coordinates to directions
def path_convert(pathc):
	pathd=""
	i=0
	j=1
	while(j<len(pathc)):
		move=(pathc[j][0]-pathc[i][0],pathc[j][1]-pathc[i][1])
		if(move==(0,1)):
			pathd+="E"
		elif(move==(1,0)):
			pathd+="S"
		elif(move==(0,-1)):
			pathd+="W"
		elif(move==(-1,0)):
			pathd+="N"
		i+=1
		j+=1
	return pathd

# Main Function
if __name__ == "__main__":
	IUB_map=parse_map(sys.argv[1])
	if(IUB_map[-1]==[]):
		IUB_map.pop()
	# Find my start position
	you_loc=[(row_i,col_i) for col_i in range(len(IUB_map[0])) for row_i in range(len(IUB_map)) if IUB_map[row_i][col_i]=="#"][0]
	lposluddy=[(row_l,col_l) for col_l in range(len(IUB_map[0])) for row_l in range(len(IUB_map)) if IUB_map[row_l][col_l]=="@"]
	if(lposluddy==[]):
		print("Inf")
		exit(0)
	pos_luddy=lposluddy[0]
	# IDA*
	threshold=0+abs(you_loc[0]-pos_luddy[0])+abs(you_loc[1]-pos_luddy[1]) # f=g+h;h is Manhattan distance from current loc to Luddy
	print("Shhhh... quiet while I navigate!")
	print("Here's the solution I found:")
	if(you_loc==pos_luddy):
		print(0)
		exit(0)	
	solution=False
	while not solution:
		solution,next_th = search1(IUB_map,threshold,pos_luddy[0],pos_luddy[1]);
		threshold=next_th
		if((not solution) and (threshold==float("inf"))):
			print("Inf")
			exit(0)
	print(solution[0],path_convert(solution[1]))

