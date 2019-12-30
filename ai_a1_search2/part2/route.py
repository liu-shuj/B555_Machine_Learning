#!/usr/local/bin/python3
# Submitted by: Shujun Liu (Username: liushuj)
from queue import PriorityQueue
import sys
def read_gps(coord_dict:dict,filename:str):
	with open(filename,'r') as f:
		while True:
			l=f.readline()
			if not l:
				break
			l=l.rstrip("\n")
			tmp=l.split(" ")
			city=tmp[0]
			lat=float(tmp[1])
			lon=float(tmp[2])
			coord_dict[city]=(lat,lon)
			
def read_roads(graph:dict,filename:str):
	with open(filename,'r') as f:
		while True:
			l=f.readline()
			if not l:
				break
			l=l.rstrip("\n")
			tmp=l.split(" ")
			src=tmp[0]
			dst=tmp[1]
			miles=float(tmp[2])
			spd=float(tmp[3])
			high=tmp[4]
			hrs=miles/spd
			gal=miles/((400*spd/150)*(1-spd/150)**4)
			if not (src in graph):
				graph[src]=set()
			graph[src].add((dst,miles,hrs,gal,high,1))
			if not (dst in graph):
				graph[dst]=set()
			graph[dst].add((src,miles,hrs,gal,high,1))
			
def ldist(coord:dict,c1:str,c2:str)->float:
	if((c1 not in coord) or (c2 not in coord)):
		return 0
	return ((coord[c1][0]-coord[c2][0])**2+(coord[c1][1]-coord[c2][1])**2)**0.5

if __name__=="__main__":
	if(len(sys.argv)<4):
		print("Usage: ./route.py [start-city] [end-city] [cost-function]")
		exit(0)
		
	coord={}
	graph={}
	if len(sys.argv)>4 and sys.argv[4]=="-h":
		read_gps(coord,"city-gps.txt")
	read_roads(graph,"road-segments.txt")

	start=sys.argv[1]
	end=sys.argv[2]
	if((start not in graph) or (end not in graph)):
		print("No results found")
		exit(0)
	if sys.argv[3]=="segments":
		h=lambda s,d:0
		COST=5
	elif sys.argv[3]=="distance":
		h=lambda s,d:ldist(coord,s,d)
		COST=1
	elif sys.argv[3]=="time":
		h=lambda s,d:ldist(coord,s,d)/65
		COST=2
	elif sys.argv[3]=="mpg":
		h=lambda s,d:ldist(coord,s,d)/33
		COST=3
	if len(sys.argv)==4:
		h=lambda x,y:0

	g={}
	for city in graph:
		g[city]=float("inf")
	g[start]=0
	hq=PriorityQueue()
	hq.put_nowait((h(start,end),0,start,start,0,0,0,0))
	FVAL=0
	GVAL=1
	PATH=2
	CITY=3
	NAME=0
	while not hq.empty():
		cur=hq.get_nowait()
		if(cur[CITY]==end):
			result="{:.0f} {:.0f} {:.4f} {:.4f} {:}".format(cur[4],cur[5],cur[6],cur[7],cur[2])
			print(result)
			exit(0)
		for adj in graph[cur[CITY]]:
			new_g=cur[GVAL]+adj[COST]
			if(new_g<g[adj[NAME]]):
				g[adj[NAME]]=new_g
				hq.put_nowait((new_g+h(adj[NAME],end),new_g,cur[PATH]+" "+adj[NAME],adj[NAME],cur[4]+1,cur[5]+adj[1],cur[6]+adj[2],cur[7]+adj[3]))
	print("Inf")
	
