import Move

# Constants representing the grid states
GOAL = -1
FREE = 0
WALL = 1
MASTER = 2
# A non-master brick is represented by a number > 2

class Puzzle:
    __slots__ = ('width', 'height', 'grid', 'numBricks', 'goal')

    def __init__(self, width, height, grid, numBricks=0, goal=[]):
        self.width = width
        self.height = height

        # Copy grid into new matrix
        self.grid = [[num for num in row] for row in grid]

        self.numBricks = numBricks
        # If number of bricks is undefined, determine it by maximum number in grid
        if numBricks == 0:
            for row in self.grid:
                self.numBricks = max(self.numBricks, max(row))
            self.numBricks -= 1

        # Goal location can be defined, otherwise it is located
        # The format is [top left row, top left col, height, width]
        # Saving the goal location allows the gameStateSolved to be done quicker
        if len(goal) == 0:
            row, col = self.findCorner(GOAL)
            if row == None and col == None:
                # Puzzle is solved
                self.goal = [0,0,0,0]
            else:
                self.goal = self.getDims(GOAL)
        else:
            self.goal = goal

    def __str__(self):
        '''Returns a string representing the puzzle'''
        puzzStr = str(self.width) + ',' + str(self.height)
        for r in xrange(self.height):
            puzzStr += '\n'
            for c in xrange(self.width):
                puzzStr += str(self.grid[r][c]) + ','
        return puzzStr

    def __hash__(self):
        '''Returns an integer that uniquely identifies this state by joining all mutable square
           values in the grid as a base [numBricks+3] integer. Each square is represented by its own
           value + 1 so a goal becomes 0, free becomes 2, master becomes 3 and so on. For 1 brick, 
           the max value is 3, corresponding to base 4 which is numBrick+3'''
        hashVal = long(0)
        for r in xrange(self.height):
            for c in xrange(self.width):
                if self.grid[r][c] != WALL:
                    hashVal *= self.numBricks + 3
                    hashVal += self.grid[r][c] + 1
        return hashVal

    def outputGameState(self):
        print self

    def gameStateSolved(self):
        '''Determines if the puzzle is solved by looking for any open goal squares'''
        for r in xrange(self.goal[2]):
            for c in xrange(self.goal[3]):
                if self.grid[r+self.goal[0]][c+self.goal[1]] == GOAL:
                    return False
        return True

    def normalizeState(self):
        '''Clones this state and renumbers all bricks to a standard format to allow for comparison'''
        normalState = clonePuzzle(self)
        brickIndex = 3
        for r in xrange(normalState.height):
            for c in xrange(normalState.width):
                if normalState.grid[r][c] == brickIndex:
                    brickIndex += 1
                elif normalState.grid[r][c] > brickIndex:
                    normalState.swapIndex(brickIndex, normalState.grid[r][c])
                    brickIndex += 1
        return normalState

    def swapIndex(self, ind1, ind2):
        '''Swaps indices of two blocks'''
        for r in xrange(self.height):
            for c in xrange(self.width):
                if self.grid[r][c] == ind1:
                    self.grid[r][c] = ind2
                elif self.grid[r][c] == ind2:
                    self.grid[r][c] = ind1

    def allMovesHelp(self, piece):
        '''Gets all moves that the given piece can make as a list of Move objects'''
        dims = self.getDims(piece)
        moves = []

        for direction in [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]:
            newDims = Move.getNewDimensions(dims, direction)
            free = True
            for r in xrange(dims[2]):
                for c in xrange(dims[3]):
                    if not self.canMove(piece, newDims[0]+r, newDims[1]+c):
                        free = False
                        break
            if free:
                moves.append(Move.Move(piece, dims, direction))

        return moves

    def allMoves(self):
        '''Gets all moves that can be made as a list of Move objects'''
        moves = []
        for i in xrange(self.numBricks):
            # Piece number is i+2
            moves.extend(self.allMovesHelp(i+2))
        return moves

    def applyMove(self, move):
        '''Makes the specified move on this puzzle state and normalizes'''
        move.apply(self.grid)

    def applyMoveCloning(self, move):
        '''Creates a new puzzle then makes specified move to the clone'''
        puzzleClone = clonePuzzle(self)
        puzzleClone.applyMove(move)
        return puzzleClone

    def findCorner(self, piece):
        '''Returns a list specifiying the position of the top left of [piece] as [row, col]'''
        
        # First find corner of piece
        for r in xrange(self.height):
            for c in xrange(self.width):
                if self.grid[r][c] == piece:
                    return [r, c]
        # Not found
        return [None, None]
                    

    def getSize(self, piece, tlr, tlc):
        '''Determines the height and width of the specified piece given its corner position'''
        # Determine height
        h = 1
        row = tlr+1
        while row < self.height and self.grid[row][tlc] == piece:
            h += 1
            row += 1

        # Determine width
        w = 1
        col = tlc+1
        while col < self.width and self.grid[tlr][col] == piece:
            w += 1
            col += 1

        return h, w

    def getDims(self, piece):
        '''Returns a four element list specifying the dimensions and position of [piece] as
           [top left corner row, top left corner col, height, width]
           given the top left corner position'''

        tlr, tlc = self.findCorner(piece)
        h, w = self.getSize(piece, tlr, tlc)
        return [tlr, tlc, h, w]

    def canMove(self, piece, r, c):
        '''Determines if the specified piece can move to a square at (r,c)'''
        if r < 0 or c < 0 or r >= self.height or c >= self.width:
            return False

        if piece > MASTER:
            return self.grid[r][c] == FREE or self.grid[r][c] == piece
        # Master piece can move to the goal
        return self.grid[r][c] == FREE or self.grid[r][c] == piece or self.grid[r][c] == GOAL 


def loadGameState(filename):
    '''Reads a puzzle file into a grid matrix and creates the blocks in the puzzle''' 

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Read dimensions from first line
    dims = lines[0].split(',')
    width = int(dims[0])
    height = int(dims[1])

    # Read grid by splitting on commas and ignoring trailing comma
    grid = [[int(x) for x in line.split(',')[0:-1]] for line in lines[1:]]

    return Puzzle(width, height, grid)

def clonePuzzle(puzzle):
    '''Creates a deep copy of the specified puzzle using the Puzzle contstructor'''
    return Puzzle(puzzle.width, puzzle.height, puzzle.grid, puzzle.numBricks, puzzle.goal)

def stateEqual(puzzle1, puzzle2):
    ''' Determines if two puzzle states are the same'''
    # Compare grid square by square
    for r in xrange(puzzle1.height):
        for c in xrange(puzzle1.width):
            if puzzle1.grid[r][c] != puzzle2.grid[r][c]:
                return False
    return True
