"""
Chess_engine.py

Stores the current state of the chess game, move validation, special moves,
undo/redo functionality, and move log.

Naming scheme:
- First letter: 'w' (white), 'b' (black)
- Second letter: 'R' (rook), 'N' (knight), 'B' (bishop), 'Q' (queen), 'K' (king), 'p' (pawn)
- '--' represents an empty square
"""


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.redoStack = []

        # Castling rights moves
        self.castleRights = [True, True, True, True]
        self.whiteKingMoved = False
        self.blackKingMoved = False
        self.whiteRookMoved = [False, False]  
        self.blackRookMoved = [False, False]

        # En passant square
        # If a pawn moves two squares forward, the square behind it is the en passant square
        self.enPassantSquare = ()

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        self.redoStack.clear()

        # Update castling rights and moved flags
        if move.pieceMoved == "wK":
            self.whiteKingMoved = True
            self.castleRights[0] = False
            self.castleRights[1] = False

        elif move.pieceMoved == "bK":
            self.blackKingMoved = True
            self.castleRights[2] = False
            self.castleRights[3] = False

        elif move.pieceMoved == "wR":
            if move.startRow == 7 and move.startCol == 0:
                self.whiteRookMoved[0] = True
                self.castleRights[1] = False
            elif move.startRow == 7 and move.startCol == 7:
                self.whiteRookMoved[1] = True
                self.castleRights[0] = False
                
        elif move.pieceMoved == "bR":
            if move.startRow == 0 and move.startCol == 0:
                self.blackRookMoved[0] = True
                self.castleRights[3] = False
            elif move.startRow == 0 and move.startCol == 7:
                self.blackRookMoved[1] = True
                self.castleRights[2] = False

        # Handle castling move
        if move.isCastleMove:
            if move.pieceMoved == "wK":
                if move.endCol == 6:  # kingside
                    self.board[7][5] = "wR"
                    self.board[7][7] = "--"
                elif move.endCol == 2:  # queenside
                    self.board[7][3] = "wR"
                    self.board[7][0] = "--"
            elif move.pieceMoved == "bK":
                if move.endCol == 6:  # kingside
                    self.board[0][5] = "bR"
                    self.board[0][7] = "--"
                elif move.endCol == 2:  # queenside
                    self.board[0][3] = "bR"
                    self.board[0][0] = "--"

        # Handle en passant capture
        if move.isEnPassantMove:
            if move.pieceMoved == "wp":
                self.board[move.endRow + 1][move.endCol] = "--"
            elif move.pieceMoved == "bp":
                self.board[move.endRow - 1][move.endCol] = "--"

        # Update en passant square
        # If a pawn moves two squares forward, the square behind it is the en passant square
        if move.pieceMoved[1] == "p" and abs(move.startRow - move.endRow) == 2:
            self.enPassantSquare = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enPassantSquare = ()

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.redoStack.append(move)
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

            # Undo castling rook move
            if move.isCastleMove:
                if move.pieceMoved == "wK":
                    if move.endCol == 6:
                        self.board[7][7] = "wR"
                        self.board[7][5] = "--"
                    elif move.endCol == 2:
                        self.board[7][0] = "wR"
                        self.board[7][3] = "--"
                elif move.pieceMoved == "bK":
                    if move.endCol == 6:
                        self.board[0][7] = "bR"
                        self.board[0][5] = "--"
                    elif move.endCol == 2:
                        self.board[0][0] = "bR"
                        self.board[0][3] = "--"

            # Undo en passant capture
            if move.isEnPassantMove:
                if move.pieceMoved == "wp":
                    self.board[move.endRow + 1][move.endCol] = "bp"
                elif move.pieceMoved == "bp":
                    self.board[move.endRow - 1][move.endCol] = "wp"



    def redoMove(self):
        if len(self.redoStack) != 0:
            move = self.redoStack.pop()
            self.makeMove(move)

    def getValidMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                color = self.board[r][c][0]
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r > 0 and self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))
            # Captures


            if r > 0 and c > 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1, c-1) == self.enPassantSquare:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEnPassantMove=True))
            if r > 0 and c < 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1, c+1) == self.enPassantSquare:
                    moves.append(Move((r,c), (r-1,c+1), self.board, isEnPassantMove=True))
        else:
            if r < 7 and self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            

            if r < 7 and c > 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1, c-1) == self.enPassantSquare:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEnPassantMove=True))
            if r < 7 and c < 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1,c+1), self.board))
                elif (r+1, c+1) == self.enPassantSquare:
                    moves.append(Move((r,c), (r+1,c+1), self.board, isEnPassantMove=True))

    def getRookMoves(self, r, c, moves):
        directions = [(-1,0), (0,-1), (1,0), (0,1)]
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        ally = 'w' if self.whiteToMove else 'b'
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r,c), (endRow,endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        enemy = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemy:
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        ally = 'w' if self.whiteToMove else 'b'
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally:
                    moves.append(Move((r,c), (endRow,endCol), self.board))
        # Castling
        self.getCastleMoves(r, c, moves)

    def getCastleMoves(self, r, c, moves):
        if self.whiteToMove:
            # Kingside
            if self.castleRights[0] and self.board[7][5] == "--" and self.board[7][6] == "--":
                if not self.squareUnderAttack(7,4) and not self.squareUnderAttack(7,5) and not self.squareUnderAttack(7,6):
                    moves.append(Move((7,4), (7,6), self.board, isCastleMove=True))
            # Queenside
            if self.castleRights[1] and self.board[7][1] == "--" and self.board[7][2] == "--" and self.board[7][3] == "--":
                if not self.squareUnderAttack(7,4) and not self.squareUnderAttack(7,3) and not self.squareUnderAttack(7,2):
                    moves.append(Move((7,4), (7,2), self.board, isCastleMove=True))
        else:
            # Kingside
            if self.castleRights[2] and self.board[0][5] == "--" and self.board[0][6] == "--":
                if not self.squareUnderAttack(0,4) and not self.squareUnderAttack(0,5) and not self.squareUnderAttack(0,6):
                    moves.append(Move((0,4), (0,6), self.board, isCastleMove=True))
            # Queenside
            if self.castleRights[3] and self.board[0][1] == "--" and self.board[0][2] == "--" and self.board[0][3] == "--":
                if not self.squareUnderAttack(0,4) and not self.squareUnderAttack(0,3) and not self.squareUnderAttack(0,2):
                    moves.append(Move((0,4), (0,2), self.board, isCastleMove=True))

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = []
        for row in range(8):
            for col in range(8):
                color = self.board[row][col][0]
                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    piece = self.board[row][col][1]
                    if piece == 'p':
                        self.getPawnAttacks(row, col, oppMoves)
                    elif piece == 'R':
                        self.getRookMoves(row, col, oppMoves)
                    elif piece == 'N':
                        self.getKnightMoves(row, col, oppMoves)
                    elif piece == 'B':
                        self.getBishopMoves(row, col, oppMoves)
                    elif piece == 'Q':
                        self.getQueenMoves(row, col, oppMoves)
                    elif piece == 'K':
                        self.getKingMoves(row, col, oppMoves)
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getPawnAttacks(self, r, c, moves):
        if self.whiteToMove:
            if r > 0 and c > 0:
                moves.append(Move((r,c), (r-1,c-1), self.board))
            if r > 0 and c < 7:
                moves.append(Move((r,c), (r-1,c+1), self.board))
        else:
            if r < 7 and c > 0:
                moves.append(Move((r,c), (r+1,c-1), self.board))
            if r < 7 and c < 7:
                moves.append(Move((r,c), (r+1,c+1), self.board))

class Move:
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnPassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isEnPassantMove = isEnPassantMove
        self.isCastleMove = isCastleMove

    def getChessMove(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
