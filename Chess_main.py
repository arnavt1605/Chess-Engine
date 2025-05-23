# Chess_main.py

import pygame as p
import Chess_engine

width = height = 512
bottom_panel_height = 100
dimension = 8
sq_size = height // dimension
max_fps = 15
images = {}
small_images = {}

def loadImages():
    global images, small_images
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        images[piece] = p.image.load("images/" + piece + ".png")
        small_images[piece] = p.transform.scale(images[piece], (32, 32))

def main():
    p.init()
    screen = p.display.set_mode((width, height + bottom_panel_height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Chess_engine.GameState()
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    validMoves = gs.getValidMoves()
    moveMade = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                if location[1] < height:
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = Chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                        for validMove in validMoves:
                            if (move.startRow == validMove.startRow and move.startCol == validMove.startCol and
                                move.endRow == validMove.endRow and move.endCol == validMove.endCol):
                                gs.makeMove(validMove)
                                moveMade = True
                                break
                        sqSelected = ()
                        playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                if e.key == p.K_y:
                    gs.redoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, sqSelected)
        drawMoveHistory(screen, gs)
        drawCapturedPieces(screen, gs)
        clock.tick(max_fps)
        p.display.flip()

def drawGameState(screen, gs, sqSelected):
    drawBoard(screen)
    highlightSquare(screen, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def highlightSquare(screen, sqSelected):
    if sqSelected != ():
        s = p.Surface((sq_size, sq_size))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        screen.blit(s, (sqSelected[1] * sq_size, sqSelected[0] * sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))

def drawMoveHistory(screen, gs):
    font = p.font.SysFont("Arial", 18, False, False)
    moveLog = gs.moveLog
    move_texts_white = []
    move_texts_black = []
    for i, move in enumerate(moveLog):
        move_str = move.getChessMove()
        if i % 2 == 0:
            move_texts_white.append(move_str)
        else:
            move_texts_black.append(move_str)
    # Draw background
    p.draw.rect(screen, p.Color("lightgray"), p.Rect(0, height, width, 40))
    # Draw move numbers and moves
    for i in range(max(len(move_texts_white), len(move_texts_black))):
        move_num = font.render(str(i+1) + ".", True, p.Color("black"))
        screen.blit(move_num, (10, height + 5 + i * 18))
        if i < len(move_texts_white):
            movew = font.render(move_texts_white[i], True, p.Color("black"))
            screen.blit(movew, (40, height + 5 + i * 18))
        if i < len(move_texts_black):
            moveb = font.render(move_texts_black[i], True, p.Color("black"))
            screen.blit(moveb, (120, height + 5 + i * 18))

def drawCapturedPieces(screen, gs):
    # White's captured (by black) on left, Black's captured (by white) on right
    y = height + 45
    # White's pieces captured (drawn as small black pieces)
    for i, piece in enumerate(gs.capturedWhite):
        screen.blit(small_images[piece], (10 + i * 36, y))
    # Black's pieces captured (drawn as small white pieces)
    for i, piece in enumerate(gs.capturedBlack):
        screen.blit(small_images[piece], (width - (i+1) * 36 - 10, y))

if __name__ == "__main__":
    main()
