Sliding Block Puzzle Solver

Compiling:
    There is nothing to compile, but there is a makefile that can be run that will run the main program.

Running:
    The file can be run with a specified search method and one or more puzzle files to solve. The command to run is:

    python main.py [search method] [files]
     -search method: This can be either "random", "depth", "breadth", "uniform" to run both depth-first and breadth first search, or "AStar" to run A* search with both Manhattan distance as a hueristic and a custom heuristic.
     -files: This can be one or more paths to a text file containing a sliding block puzzle

Custom Heuristic:
    The custom heuristic used counts the number of open squares in the area between the master brick and the goal (i.e. the area containing all paths of the Manhattan cost). This number is subtracted from the Manhattan cost to get the number of squares that must be freed. This is divided by the longest side length of the bricks in this area as this is the number of squares that can be freed in one move. Then the Manhattan distance is added because this is the number of moves of the master brick that is required

Results:
    The results of running A* search with both heuristics on all specified puzzles are included in "output-part2.txt". This can be replicated by running
    python main.py uniform SBP-bricks-level0.txt SBP-bricks-level1.txt SBP-bricks-level2.txt SBP-bricks-level3.txt SBP-bricks-level4.txt SBP-bricks-level5.txt SBP-bricks-level6.txt SBP-bricks-level7.txt