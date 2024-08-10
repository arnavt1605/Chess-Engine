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


    def makeMove(self, move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]= move.pieceMoved
        self.moveLog.append(move)

class Move():
    #Mapping the key value pairs of the dictionaries to match the naming of the squares in real life as well in accrding to the code. 
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks= {v: k for k, v in ranksToRows.items()}
    filesToCols= {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles= {v: k for k, v in filesToCols.items()}





    def __init__(self, startSq, endSq, board):
        self.startRow= startSq[0]
        self.startCol= startSq[1]
        self.endRow= endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved= board[self.startRow][self.startCol]  #To keep track of the piece moved
        self.pieceCaptured= board[self.endRow][self.endCol]    #To keep track of the piece captured

    def getChessMove(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
