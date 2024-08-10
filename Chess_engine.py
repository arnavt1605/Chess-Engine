# This class is responsible for storing the current state of a chess game. 
# It will also be responsible for determining the valid moves for the current state.
# A move log will also be made and maintained.

'''
Naming Scheme of the pieces: First letter represents the colour of the piece: w for white and b for black.
Next letter represents the type of piece: R for rook, N for knight, B for bishop, Q for queen, K for king, p for pawns.
-- represents an empty square
'''

class GameState():
    def __init__(self):
        self.board=[
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR" ],
            ["bp","bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp","wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR" ]]
        self.whiteToMove=True 
        self.moveLog= []    # To keep track of the previous moves.

class Move():

    def __init__(self, startSq, endSq, board):
        