#!/usr/bin/env python

import sys
import Puzzle
from RandomWalk import RandomWalk
from DepthFirstSearch import DepthFirstSearch
from BreadthFirstSearch import BreadthFirstSearch
from AStarSearch import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: python main.py [random/depth/breadth/uniform] [filenames]'
        sys.exit(0)
    else:
        for filename in sys.argv[2:]:
            puzzle = Puzzle.loadGameState(filename)
            if sys.argv[1] == 'random':
                print '\nSearching ' + filename + ' by a random walk\n'
                print puzzle
                randomWalker = RandomWalk(puzzle)
                randomWalker.search()
            elif sys.argv[1] == 'depth':
                print '\nSolving ' + filename + ' by depth-first search\n'
                print puzzle
                searcher = DepthFirstSearch()
                searcher.solve(puzzle)
                print depthSearcher.getStatistics()
            elif sys.argv[1] == 'breadth':
                print '\nSolving ' + filename + ' by breadth-first search\n'
                print puzzle
                searcher = BreadthFirstSearch()
                searcher.solve(puzzle)
                print searcher.getStatistics()
            elif sys.argv[1] == 'uniform':
                print '\nSolving ' + filename + ' by depth-first search\n'
                print puzzle
                searcher = DepthFirstSearch()
                searcher.solve(puzzle)
                print searcher.getStatistics()

                print '\nSolving ' + filename + ' by breadth-first search\n'
                print puzzle
                searcher = BreadthFirstSearch()
                searcher.solve(puzzle)
                print searcher.getStatistics()
            elif sys.argv[1] == 'AStar':
                print '\nSolving ' + filename + ' by A* search with Manhattan distance heuristic\n'
                print puzzle
                searcher = AStarSearch(manhattanCost)
                searcher.solve(puzzle)
                print searcher.getStatistics()

                print '\nSolving ' + filename + ' by A* search with custom heuristic\n'
                print puzzle
                searcher = AStarSearch(blockageCost)
                searcher.solve(puzzle)
                print searcher.getStatistics()
            else:
                print 'Usage: python main.py [random/depth/breadth/uniform] [filenames]'
                sys.exit(0)