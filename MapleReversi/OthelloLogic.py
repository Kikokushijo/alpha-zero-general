'''
Author: Eric P. Nichols
Modified: Chia-Wei, Liu (kikokushijo@github)
Date: Feb 8, 2008., Jun 30, 2019(Maplestory ver.)
Board class.
Board data:
  1=white, -1=black, 0=EMPTY_SYMBOL, 2=obstacle
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x, y) tuples.
x is the column, y is the row.
'''
import numpy as np

class Board():

    # List of all 8 directions on the board, as (x, y) offsets
    __directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]

    # define piece category
    # Notice: assert WHITE_SYMBOL == -BLACK_SYMBOL
    WHITE_SYMBOL = 1
    BLACK_SYMBOL = -1
    EMPTY_SYMBOL = 0
    OBSTACLE_SYMBOL = 2

    def __init__(self, n, obstacles=None):
        "Set up initial board configuration."

        self.n = n
        if self.n % 2:
            raise ValueError("Board size should be 2n * 2n.")

        # Create the empty board array.
        self.pieces = np.zeros((self.n, self.n), dtype=np.int8)

        # Set up the initial 4 pieces.
        self.pieces[self.n//2-1][self.n//2] = self.WHITE_SYMBOL
        self.pieces[self.n//2][self.n//2-1] = self.WHITE_SYMBOL
        self.pieces[self.n//2-1][self.n//2-1] = self.BLACK_SYMBOL
        self.pieces[self.n//2][self.n//2] = self.BLACK_SYMBOL

        # Set up obstacles.
        self.obstacles = obstacles
        if self.obstacles:
            for obstacle in obstacles:
                # Turn human-reading coordinates to numpy dimensions.
                if self.pieces[obstacle] != self.EMPTY_SYMBOL:
                    raise ValueError("Duplicated obstacles or obstacles on the central 4 pieces.")
                self.pieces[obstacle] = self.OBSTACLE_SYMBOL

    # Add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]
    
    def __setitem__(self, key, value):
        self.pieces[key] = value

    def countPieces(self, color):
        """Counts the # pieces of the given color
        (1 for white, -1 for black, 0 for empty spaces, 2 for obstacles)"""
        return np.count_nonzero(self.pieces == color)
    
    def evaluateDiff(self, player):
        return self.countPieces(player) - self.countPieces(-player)


    def get_legal_moves(self, color):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        """
        # Store the legal moves.
        moves = set()

        # Get all the squares with pieces of the given color.
        for x_idx, row in enumerate(self.pieces):
            for y_idx, piece in enumerate(row):
                if piece == color:
                    newmoves = self.get_moves_for_square((x_idx, y_idx))
                    moves.update(newmoves)
        return list(moves)

    def has_legal_moves(self, color):
        for x_idx, row in enumerate(self.pieces):
            for y_idx, piece in enumerate(row):
                if piece == color:
                    newmoves = self.get_moves_for_square((x_idx, y_idx))
                    if newmoves:
                        return True
        return False

    def get_moves_for_square(self, square):
        """Returns all the legal moves that use the given square as a base.
        That is, if the given square is (3,4) and it contains a black piece,
        and (3,5) and (3,6) contain white pieces, and (3,7) is empty, one
        of the returned moves is (3,7) because everything from there to (3,4)
        is flipped.
        """

        # Determine the color of the piece.
        color = self[square]

        # Skip empty / obstacle source squares.
        if color in [self.EMPTY_SYMBOL, self.OBSTACLE_SYMBOL]:
            return None

        # search all possible directions.
        moves = []
        for direction in self.__directions:
            move = self._discover_move(square, direction)
            if move:
                moves.append(move)

        # return the generated move list
        return moves

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """

        # Much like move generation, start at the new piece's square and
        # follow it on all 8 directions to look for a piece allowing flipping.

        # Add the piece to the EMPTY_SYMBOL square.
        flips = [flip for direction in self.__directions
                      for flip in self._get_flips(move, direction, color)]
        assert flips
        for flip in flips:
            self[flip] = color

    def _discover_move(self, origin, direction):
        """ Returns the endpoint for a legal move, starting at the given origin,
        moving by the given increment."""

        color = self[origin]

        flips = []
        for move in Board._increment_move(origin, direction, self.n):
            if self[move] == self.EMPTY_SYMBOL:
                if flips:
                    return move
                else:
                    return None
            elif self[move] in [color, self.OBSTACLE_SYMBOL]:
                return None
            elif self[move] == -color:
                flips.append(move)
        return None

    def _get_flips(self, origin, direction, color):
        """ Gets the list of flips for a vertex and direction to use with the
        execute_move function """
        #initialize variables
        flips = [origin]

        for move in Board._increment_move(origin, direction, self.n):
            if self[move] in [self.EMPTY_SYMBOL, self.OBSTACLE_SYMBOL]:
                return []
            if self[move] == -color:
                flips.append(move)
            elif self[move] == color and flips:
                return flips
        return []

    @staticmethod
    def _increment_move(move, direction, n):
        # print(move)
        """ Generator expression for incrementing moves """
        move = list(map(sum, zip(move, direction)))
        #move = (move[0]+direction[0], move[1]+direction[1])
        while all(map(lambda x: 0 <= x < n, move)): 
        #while 0<=move[0] and move[0]<n and 0<=move[1] and move[1]<n:
            yield move
            move = list(map(sum, zip(move, direction)))
            #move = (move[0]+direction[0],move[1]+direction[1])

