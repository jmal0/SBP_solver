from Search import Search, MoveNode
import Puzzle
import Move
import Queue

class AStarSearch(Search):

    def __init__(self, costFunction):
        Search.__init__(self)
        self.moveQueue = Queue.PriorityQueue()
        self.cost = costFunction

    def search(self, state):
        '''Searches nodes in order of expected cost to reach the goal'''
        startNode = self.addState(state, None, None, self.cost(state))
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
                childNode = self.addState(childState, move, currentNode, self.cost(childState))
                self.moveQueue.put(childNode)

    def addState(self, state, move=None, parentNode=None, hcost=0):
        '''Adds a state to the search tree and searched nodes. Returns the node for this state'''
        normalState = state.normalizeState()
        self.states.add(hash(normalState))
        return AStarNode(state, move, parentNode, self.cost(state))

    def checkState(self, state):
        '''Determines if a state has been reached in the search'''
        return hash(state.normalizeState()) in self.states

def manhattanCost(state):
    '''Returns the sum of horizontal and vertical moves to get the master brick to the goal'''
    # Take distance between closer corners
    [rows, cols] = manhattanComponents(state)
    return rows + cols

def manhattanComponents(state):
    '''Determine distance in horizontal and vertical directions to goal'''
    # Get dimensions and location of master
    master = state.getDims(Puzzle.MASTER)

    # Take distance between closer corners
    rows = min(abs(master[0] - state.goal[0]), abs(master[0]+master[2] - (state.goal[0] + state.goal[2])))
    cols = min(abs(master[1] - state.goal[1]), abs(master[1]+master[3] - (state.goal[1] + state.goal[3])))
    return [rows, cols]

def weightedCost(state):
    return 0.25*manhattanCost(state) + 0.75*blockageCost(state)

def blockageCost(state):
    '''Determines the fraction of positions occupied by blocks in the area between the master brick 
       and the goal and normalizes it by manhattan distance to approximate the relative expected 
       cost to the goal'''
    [startRow, endRow, startCol, endCol] = getManhattanArea(state)

    # Count bricks
    countBricks = 0.0
    for r in xrange(startRow, endRow+1, 1):
        for c in xrange(startCol, endCol+1, 1):
            if state.grid[r][c] >= Puzzle.MASTER:
                countBricks += 1

    # Score is numBricks/maxBricks*(manhattanCost - 1) + 1
    # Always at least one move to goal so normalize by Manhattan distance - 1 and add 1
    return countBricks/((endCol-startCol+1)*(endRow-startRow+1)) * (manhattanCost(state) - 1) + 1

def blockageCost(state):
    '''Determines the fraction of positions occupied by blocks in the area between the master brick 
       and the goal and normalizes it by manhattan distance to approximate the relative expected 
       cost to the goal'''
    [startRow, endRow, startCol, endCol] = getManhattanArea(state)

    # Count open squares
    countOpen = 0.0
    maxArea = 1
    for r in xrange(startRow, endRow+1, 1):
        for c in xrange(startCol, endCol+1, 1):
            if state.grid[r][c] >= Puzzle.MASTER:
                dims = state.getDims(state.grid[r][c])
                if dims[2]*dims[3] > maxArea:
                    maxArea = dims[2]*dims[3]
            elif state.grid[r][c] == Puzzle.FREE:
                countOpen += 1

    # Score is numBricks/maxBricks*(manhattanCost - 1) + 1
    # Always at least one move to goal so normalize by Manhattan distance - 1 and add 1
    return max(0,(manhattanCost(state) - countOpen))/maxArea + manhattanCost(state)

def movableManhattanCost(state):
    '''Adds 1 to Manhattan distance if master brick cannot currently make a useful move'''
    # Get dimensions and location of master
    pos = state.getDims(Puzzle.MASTER)
    # Get moves master brick can make and check if it includes move that will decrease distance
    movesMaster = state.allMovesHelp(Puzzle.MASTER)
    cost = 1 # If no moves are found, it will take at least one more move to reach goal
    for move in movesMaster:
        newPos = [pos[0]+Move.DIRECTIONS[move.dir][0], pos[1]+Move.DIRECTIONS[move.dir][1]]
        # See if new position brings x or y closer
        if abs(newPos[0] - state.goal[0]) < abs(pos[0] - state.goal[0]) or abs(newPos[1] - state.goal[1]) < abs(pos[1] - state.goal[1]):
            cost = 0
            break
    return manhattanCost(state) + cost

def pathCountCost(state):
    '''Count all paths in the Manhattan area, i.e. the number of paths connecting vertices in the 
       graph of the state space'''
    [startRow, endRow, startCol, endCol] = getManhattanArea(state)

    pathCountV = 0
    for r in xrange(startRow, endRow, 1):
        for c in xrange(startCol, endCol+1, 1):
            # Can a block be moved downward
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER) and (state.grid[r+1][c] == Puzzle.FREE or state.grid[r+1][c] == Puzzle.MASTER):
               pathCountV += 1
    pathCountH = 0
    for r in xrange(startRow, endRow+1, 1):
        for c in xrange(startCol, endCol, 1):
            # Can a block be moved to the right
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER) and (state.grid[r][c+1] == Puzzle.FREE or state.grid[r][c+1] == Puzzle.MASTER):
               pathCountH += 1

    # Get dimensions and location of master
    dimsMaster = state.getDims(Puzzle.MASTER)
    [rows, cols] = manhattanComponents(state)
    # Determine how many paths are needed to move the master brick to the goal
    pathsHNeeded = rows*dimsMaster[2]
    pathsVNeeded = cols*dimsMaster[3]
    # Return the defecit in paths available plus the number of moves required
    return max(1, min(rows, (pathsVNeeded - pathCountV)) + min(cols, (pathsHNeeded - pathCountH)))

def pathCountCost3(state):
    '''Count all paths in the Manhattan area, i.e. the number of paths connecting vertices in the 
       graph of the state space'''
    
    pathCountV = 0
    for r in xrange(state.height-1):
        for c in xrange(state.width):
            # Can a block be moved downward
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL) and (state.grid[r+1][c] == Puzzle.FREE or state.grid[r+1][c] == Puzzle.MASTER or state.grid[r+1][c] == Puzzle.GOAL):
               pathCountV += 1
    pathCountH = 0
    for r in xrange(state.height):
        for c in xrange(state.width-1):
            # Can a block be moved to the right
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL) and (state.grid[r][c+1] == Puzzle.FREE or state.grid[r][c+1] == Puzzle.MASTER or state.grid[r][c+1] == Puzzle.GOAL):
               pathCountH += 1

    # Get dimensions and location of master
    dimsMaster = state.getDims(Puzzle.MASTER)
    [rows, cols] = manhattanComponents(state)
    # Determine how many paths are needed to move the master brick to the goal
    pathsHNeeded = rows*dimsMaster[2]
    pathsVNeeded = cols*dimsMaster[3]
    # Return the defecit in paths available plus the number of moves required
    #return pathsVNeeded/pathCountV*cols + pathsHNeeded/pathCountV*rows
    return (cols + rows)*(pathsHNeeded+pathsVNeeded)/(pathCountH+pathCountV)

def pathCountCost2(state):
    '''Count all paths in the Manhattan area, i.e. the number of paths connecting vertices in the 
       graph of the state space'''
    [startRow, endRow, startCol, endCol] = getManhattanArea(state)

    pathCountV = 0
    for r in xrange(startRow, endRow, 1):
        for c in xrange(startCol, endCol+1, 1):
            # Can a block be moved downward
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL) and (state.grid[r+1][c] == Puzzle.FREE or state.grid[r+1][c] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL):
               pathCountV += 1
    pathCountH = 0
    for r in xrange(startRow, endRow+1, 1):
        for c in xrange(startCol, endCol, 1):
            # Can a block be moved to the right
            if (state.grid[r][c] == Puzzle.FREE or state.grid[r][c] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL) and (state.grid[r][c+1] == Puzzle.FREE or state.grid[r][c+1] == Puzzle.MASTER or state.grid[r][c] == Puzzle.GOAL):
               pathCountH += 1

    # Get dimensions and location of master
    dimsMaster = state.getDims(Puzzle.MASTER)
    [rows, cols] = manhattanComponents(state)
    # Determine how many paths are needed to move the master brick to the goal
    pathsHNeeded = rows*dimsMaster[2]
    pathsVNeeded = cols*dimsMaster[3]

    if pathsVNeeded + pathsHNeeded <= pathCountH + pathCountV:
        return manhattanCost(state)
    else:
        return manhattanCost(state) + 1

def getManhattanArea(state):
    '''Returns the bounding rows and columns of the area containing all paths of the Manhattan
       distance in length to the goal'''
    # Get dimensions and location of master
    master = state.getDims(Puzzle.MASTER)
    
    # Determine the range of rows to check for bricks
    if abs(master[0] - state.goal[0]) > abs(master[0]+master[2] - (state.goal[0] + state.goal[2])):
        # Master is left of goal, go from left side of master to right side of goal
        startRow = min(master[0], state.goal[0] + state.goal[2] - 1)
        endRow = max(master[0], state.goal[0] + state.goal[2] - 1)
    else:
        # Master is right of goal, go from left side of goal to right side of master
        startRow = min(state.goal[0], master[0] + master[2] - 1)
        endRow = max(state.goal[0], master[0] + master[2] - 1)

    # Determine the range of columns to check for bricks
    if abs(master[1] - state.goal[1]) < abs(master[1]+master[3] - (state.goal[1] + state.goal[3])):
        # Master is above goal, go from top of master to bottom of goal
        startCol = min(master[1], state.goal[1] + state.goal[3] - 1)
        endCol = max(master[1], state.goal[1] + state.goal[3] - 1)
    else:
        # Master is below goal, go from top of goal to bottom of master
        startCol = min(state.goal[1], master[1] + master[3] - 1)
        endCol = max(state.goal[1], master[1] + master[3] - 1)

    return [startRow, endRow, startCol, endCol]

class AStarNode(MoveNode):

    def __init__(self, state, move=None, parent=None, hScore=0):
        MoveNode.__init__(self, state, move, parent)
        # g will hold the move depth of this node
        if parent is None:
            # If there is no parent, initialize g at 0
            self.g = 0
        else:
            self.g = parent.g + 1
        self.f = self.g + hScore

    def __cmp__(self, other):
        '''Compares based on f cost for proper entry into priority queue'''
        return cmp(self.f, other.f)
