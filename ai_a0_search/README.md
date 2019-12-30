# a0

Shujun Liu
(Username:liushuj)

- Part I

	Search abstraction:
	- States: All possible coordinates of the walker
	- Successor function: Walk one step towards the directions that has no obstacle ahead among four directions 
	- Cost function: 1
	- Goal state: The coordinate of Luddy "@"
	- Initial state: The coordinate of me "#"

	Why does the program often fail to find a solution?

		The program uses a stack as fringe i.e. it uses DFS, but the grid is an undirected connected graph and explored states are not recorded, which means the DFS will easily add to the stack and finally go back to: a state it searched before.

	What did I do?

		I implemented an IDA*(Iterative Deepening A*) algorithm, which limits the search depth by limiting f=g+h. h() here in the code is the Manhattan distance to the goal. Additionally during the search I record the path walked up to now and ignore a successor if it is already in the path. As of recording path, one thing needed is to delete the dead ends in the path. I implemented this by recording the parents of a newly explored node on the stack and tracing back through the stack when a dead end occurs and the last few steps on the path should be deleted.

- Part II
	
	The obstacles split the floors into certain number of vertical and horizontal intervals. If a friend is put at the intersection of a horizontal and a vertical interval, the two intervals cannot hold anyone else. Thus the problem is to find as many pair of vertical and horizontal intervals as possible that there are no two pairs using a same interval. In the code this is done by DFS, with a pruning that backtracking is performed immediately when a conflict between two friends happens, avoiding searching redundant or duplicate states.


	Search abstraction:
	- States: Intervals remaining unused and coordinates of friends that already found a place
	- Successor function: Put one more friend on next available intersection and invalidate the two intervals
	- Cost function: 1
	- Goal state: K friends are on the board
	- Initial state: All horizontal and vertical intervals and no people on the board

*Ideas of part II referred to https://www.iarcs.org.in/inoi/online-study-material/problems/placing-rooks-soln.php ; implemented all by myself.



        -- Below an obsolete version of Part II (in hide1.py.old) --

	~~In this part I wrote a program that randomly put the K friends on the board and keep moving the friend with most conflicts randomly trying to find a place with smaller conflict.~~  

 	~~Search abstraction:~~

	~~- States: All possible configurations of a board with K friends~~

	~~- Successor function: All configurations that one friend with most conflicts is moved~~

	~~- Cost function: 1~~

	~~- Goal state: The configuration that no one meets each other~~

	~~- Initial state: A random configuration of K friends on board~~
