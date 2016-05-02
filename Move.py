import Puzzle

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

DIRECTIONS = {UP:[-1, 0], DOWN:[1, 0], LEFT:[0, -1], RIGHT:[0, 1]}

class Move:

    def __init__(self, piece, dimensions, direction):
        self.piece = piece
        # [top left row, top left col, height, width]
        self.dims = dimensions
        self.dir = direction

    def __str__(self):
        moveStr = '(' + str(self.piece) + ','
        if self.dir == UP:
            moveStr += 'up'
        elif self.dir == DOWN:
            moveStr += 'down'
        elif self.dir == LEFT:
            moveStr += 'left'
        else:
            moveStr += 'right'
        return moveStr + ')'


    def apply(self, grid):
        # Set vacated space to be free
        for r in xrange(self.dims[2]):
            for c in xrange(self.dims[3]):
                grid[self.dims[0]+r][self.dims[1]+c] = Puzzle.FREE

        # Move the top corner to its new position
        newDims = getNewDimensions(self.dims, self.dir)
        # Fill the grid with the piece's new position
        for r in xrange(self.dims[2]):
            for c in xrange(self.dims[3]):
                grid[newDims[0]+r][newDims[1]+c] = self.piece

def getNewDimensions(dims, direction):
    '''Takes a four element list specifying the dimensions of a block and returns a list of what the
       dimensions will be after a move in the specified direction is applied'''
    tlr = dims[0] + DIRECTIONS[direction][0]
    tlc = dims[1] + DIRECTIONS[direction][1]
    return [tlr, tlc, dims[2], dims[3]]
