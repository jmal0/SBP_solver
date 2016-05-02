import random
import AStarSearch

class RandomWalk:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getMove(self):
        moves = self.puzzle.allMoves()
        index = random.randint(0,len(moves)-1)
        return moves[index]

    def search(self, maxMoves=1000):
        for i in xrange(maxMoves):
            print self.puzzle
            print AStarSearch.blockageCost(self.puzzle)
            if self.puzzle.gameStateSolved():
                return
            move = self.getMove()
            print move
            self.puzzle.applyMove(move)
