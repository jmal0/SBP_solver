import time

class Search(object):

    def __init__(self):
        self.states = set()
        self.solutionTime = [0, 0]
        self.solutionLength = -1
        self.nodesExplored = 0

    def addState(self, state, move=None, parentNode=None):
        '''Adds a state to the search tree and searched nodes. Returns the node for this state'''
        normalState = state.normalizeState()
        self.states.add(hash(normalState))
        return MoveNode(state, move, parentNode)

    def checkState(self, state):
        '''Determines if a state has been reached in the search'''
        return hash(state.normalizeState()) in self.states
        
    def solve(self, startState):
        # Record start time
        self.solutionTime[0] = time.time()

        # Solve the puzzle and get the node to the last state
        finalNode = self.search(startState)
        self.solutionLength = len(finalNode.traceback())
        # Record end time
        self.solutionTime[1] = time.time()

        # Traceback returns list of moves in the reverse order in which they were made
        for move in reversed(finalNode.traceback()):
            print move

        print finalNode.state

    def getStatistics(self):
        '''Returns a string summarizing the solution statistics: nodes explored, time elapsed, and 
           length of solution'''
        statisticsStr = 'Nodes explored: ' + str(self.nodesExplored)
        statisticsStr += '\nTime taken: %.6f seconds' % (self.solutionTime[1]-self.solutionTime[0])
        statisticsStr += '\nSolution length: ' + str(self.solutionLength) + ' moves'
        return statisticsStr

class MoveNode:
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.move = move
        self.parent = parent

    def traceback(self):
        '''Returns a list of moves starting at the current move and ending at the root'''
        moves = []
        currentNode = self
        # Traverse tree from bottom to top and add move made to get from node to node at each step
        while currentNode.move is not None:
            moves.append(currentNode.move)
            currentNode = currentNode.parent
        return moves
