# Assignment 1
by Shujun Liu
(Username: liushuj)

- Part 1:

  The code uses A* search to search for solution. 
  
  Heuristic function for "original" is sum of Manhattan distances of all tiles in current state from its current position to its goal position.
  
  Heuristic function for "circular" is total number of misplaced tiles in the current state.
  
  Heuristic function for "luddy" is sum of Manhattan distances divided by 3.
  
  "original" supports no-solution detecting.
  
  All heuristic functions are admissible, so optimal solution is guranteed.
  
  For "original" case, possible improvements could be obtained by using other heuristic functions, such as Walking Distance(http://www.ic-net.or.jp/home/takaken/e/15pz/wd.gif), database-based heuristics(e.g. https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2209.pdf), or neural networks(https://medium.com/breathe-publication/solving-the-15-puzzle-e7e60a3d9782).
  
  
- Part 2:

  Code of Part 2 also uses A* search to find the best route.
  
  However, by default the heuristic function always equals to 0. Heuristics based on the GPS data could be enabled by adding a "-h" option after all arguments in the command line, e.g. 
  
  ./route.py Denver,_Colorado New_York,_New_York mpg -h
  
  The reason why it is not default is that I found reading in city-gps.txt takes a lot of time, this time is even longer than the time needed to navigate without heuristics. 
  
  The heuristic function for option "distance" is euclidean distance from a city to the goal calculated using latitudes and longitudes.
  
  The heuristic function for option "time" is euclidean distance divided by 65, the highest speed limit in the database.
  
  The heuristic function for option "mpg" is euclidean distance divided by 33, which is near to a local maximum value of the MPG function while v ranges from 0 to 65: MPG(30)=32.768.
  
- Part 3:

  In code of Part 3, the solve(i,b) function searches for the maximum skill point one can obtain by the first i people in the list and b EYDs.
  
  For each people, a choice of whether to hire him is made. If he is hired, the budgets is spent and skill point increases. If he is not hired, then all things stays the same as only selecting from the first i-1 people without him.
  
  The result of solve(i,b) for the i's and b's already calculated is stored so the computation could be speeded up. But this may not work well when there are too many possible b's.
  
  When computing, all skill and cost is amplified by 100000 and rounded to avoid issues caused by floating point precision, although this might be problematic in some data.
  
  After computation, the people selected could be inferred by looking at the stores. If the final result of skill points "res" could be get using a certain budget "b" appears both on store of the last people and the second last people, then it can be known that this result comes out when calculating for the second last people. Otherwise, the last people is used; this is recorded and "res" and "b" subtracting his skill and cost is used to continue this backtracking, all the way to the first people in the list.
