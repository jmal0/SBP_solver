from Search import Search
import Queue

class BreadthFirstSearch(Search):

    def __init__(self):
        Search.__init__(self)
        self.moveQueue = Queue.Queue()

    def search(self, state):
        '''Searches all child nodes of the current state'''
        startNode = self.addState(state)
        self.moveQueue.put(startNode)

        while not self.moveQueue.empty():
            # Get the next node to consider
            currentNode = self.moveQueue.get()
            currentState = currentNode.state
            self.nodesExplored += 1

            # If this state is the solution, return this state
            if currentState.gameStateSolved():
                return currentNode

            # Add each child of this node if it is new
            for move in currentState.allMoves():
                # Create new state and node by applying move
                childState = currentState.applyMoveCloning(move)
                # Check if this state has been visited, skip if it has
                if self.checkState(childState):
                    continue
                # This is a new state, add it to the tree
                childNode = self.addState(childState, move, currentNode)
                self.moveQueue.put(childNode)
