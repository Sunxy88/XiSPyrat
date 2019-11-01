Created by **Xi SONG** in IMT Atlantique, Brest, 05/09/2019

---

This repository is created for the course ***Algorithm and Discrete Mathematics*** in FISE A1S1.

All code for the creation of my AI will be showed in thie repository.

Talk is cheap! I will show you my code.

+ **Lab1**: Program a rat that moves randomly while avoiding walls
  + Code admitted: *improved_random.py* at 06/09/2019, *DataAnalyse.py* at 11/09/2019
  + Question found: 
    + In the project PyRat, a file named *random.py* which may cause problems in importing library *numpy*
  + Skill learned:
    + Meet library *numpy*
	+ Meet library *matpltlib*
  + Lessons:
    + Read source code *pyrat.py* is necessary

+ **Lab2**: Implement a BFS under the condition of unweighted graphs
  + Code admitted: *BFS_move.py* at 15/09/2019, *DFS_move.py* at 16/09/2019, *IDDFS_move.py* at 21/09/2019
  + With the will to automatically analyse the code, update *AutomaticGetStatistics.sh* (**ATTENTION**: This script may not be useful in Windows)
  + Question found:
    + (**Solved**) Every turn, main program calls function *turn*, however I wrote the code with the imagination that only one call of this function and the pause of this thread. So it is necessary to make this code correct. -> Use a file *instructions.txt* to guide the rat
  	+ (**Solved**) While coding the DFS, the recursion can not be terminated. -> Have to clearly understand the termination condition for a recursion function
  	+ (**Solved**) In beam search, which cost fonction should be chosen for the heuristic cost? **Maybe** <u>Euclidean distance</u> is a good choice
  	+ (**Solved**) Also in beam search, how should we choose an approprate beam width, for 3 at most? For this reason, I am wandering if it is practical to use beam search in this game. -> It is not interesting
  	+ (**Solved**) In shell script, how to automatically kill the process elegantly? -> No need, *pyrat.py* offer a setting to do the test
  + Lessons learned:
    + Before starting to code, it is vital to understand clearly the demand
  	+ In every recursion function, we must shrewdly consider all the possible conditions for the determination of a recursion or we will get lost and a stack overflow
  	+ Use Shell script to automatically do something interesting

+ **Lab3**: Implement Dijkstra's algorithm
  + Code admitted: *Dijkstra_move* at 25/09/2019, *AutomaticGetStatistics.sh* at 26/09/2019
  + Question found:
    +  (**Solved**) Whilte trying to use *heapq.heappush(priorityQ, (, ))*, the order of the element containing tuple is not logical. -> Actually, *heapq.heappush()* use *\_\_ls\_\_()* to decide the order in a list
  + Lessons learned:
    + Meet *heapq*, and understand how it decides the order of a heap
    + Reload operators
    + In binary balance tree (AVL Tree), two kinds of rorations (**hard to under stand** and [click here](https://en.wikipedia.org/wiki/AVL_tree) to know more) are used to keep the **balance factor** under 2

+ **Lab4**: Implement bruteforce and backtracking algorithm to get multiple pieces of cheese
  + Code admitted: *BruteForce_move.py* at 01/10/2019, *Backtracking_move.py* at 01/10/2019 and *NaiveGreedy.py*

+ **Lab5**: Implement heuristic to speed up the preprocessing
	+ Code admitted: *GeneticAlgorithm.py* at 10/10/2019
	+ Question found:
		+ Results of *GeneticAlgorithm* is not that good, have to tune parameters to make it faster and solutions better
	+ Lessons learned:
		+ Genetic algorithm can provide a solution of a question even we only know how to judge a solution

+ **Lab6**: Refactor the genetic algorithm in speeding up to get a metagraph, so it is practical to use genetic graph in maze where there are 41 cheeses.
	+ Code admitted: *Winner.py* at 01/11/2019
	+ Question found:
		+ The implementation of dijkstra before (in which I use heapq) is in a way much slower than the implementation now, maybe there is something redundant calculations.
	+ Lessons learned:
		+ It is meaningless to optimize your code before it is done, and also not useful to optimize some minor details. Doing so only makes your code hard to read and confusing.
	+ Work could be done:
		+ To tune the parameters in the genetic algorithm could be annoying, should find a way to do it elegently and efficiently.
---
**Xidian University / IMT Atlantique**
