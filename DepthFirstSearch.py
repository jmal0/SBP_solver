from Search import Search

class DepthFirstSearch(Search):

    def __init__(self):
        Search.__init__(self)
        self.moveStack = []

    def search(self, state):
        '''Searches all child nodes of the start node by expanding the children of a node first'''
        startNode = self.addState(state)
        self.moveStack.append(startNode)

        while len(self.moveStack) != 0:
            # Get the next node to consider
            currentNode = self.moveStack.pop()
            currentState = currentNode.state
            self.nodesExplored += 1

            # If this state is the solution, return this state
            if currentState.gameStateSolved():
                return currentNode

            # Add each child of this node if it is new
            for move in reversed(currentState.allMoves()):
                # Create new state and node by applying move
                childState = currentState.applyMoveCloning(move)
                # Check if this state has been visited, skip if it has
                if self.checkState(childState):
                    continue
                # This is a new state, add it to the tree
                childNode = self.addState(childState, move, currentNode)
                self.moveStack.append(childNode)
