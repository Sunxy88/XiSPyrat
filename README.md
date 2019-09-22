Created by **Xi SONG** in IMT Atlantique, Brest, 05/09/2019

---

This repository is created for the course ***Algorithm and Discrete Mathematics*** in FISE A1S1.

All code for the creation of my AI will be showed in thie repository.

Talk is cheap! I will show you my code.

+ **Lab1**: Program a rat that moves randomly while avoiding walls
  + Code admitted: improved_random.py at 06/09/2019, DataAnalyse.py at 11/09/2019
  + Question found: 
    + In the project PyRat, a file named *random.py* which may cause problems in importing library *numpy*
  + Skill learned:
    + Meet library *numpy*
	+ Meet library *matpltlib*
  + Lessons:
    + Read source code *pyrat.py* is necessary

+ **Lab2**: Implement a BFS under the condition of unweighted graphs
  + Code admitted: BFS_rome.py at 15/09/2019
  + Question found:
    + (**Solved**) Every turn, main program calls function *turn*, however I wrote the code with the imagination that only one call of this function and the pause of this thread. So it is necessary to make this code correct. -> Use a file *instructions.txt* to guide the rat
	+ While coding the DFS, the recursion can not be terminated. -> Have to clearly understand the termination condition for a recursion function
	+ In beam search, which cost fonction should be chosen for the heuristic cost? Maybe Euclidean distance is a good choice.
	+ Also in beam search, how should we choose an approprate beam width, for 3 at most? For this reason, I am wandering if it is practical to use beam search in this game.
  + Lessons learned:
    + Before starting to code, it is vital to understand clearly the demand
	+ In every recursion function, we must shrewdly consider all the possible conditions for the determination of a recursion or we will get lost and a stack overflow.
---
**Xidian University / IMT Atlantique**
