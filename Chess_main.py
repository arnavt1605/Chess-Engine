# Chess_main.py

# Main driver file for user input and displaying the current state of the game
#Will run this file to play the game

import pygame as p
import Chess_engine

width = height = 512
dimension = 8  # 8x8 chessboard
sq_size = height // dimension
max_fps = 15
images = {}

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        images[piece] = p.image.load("images/" + piece + ".png")

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = Chess_engine.GameState()
    loadImages()
    running = True
    sqSelected = ()  # No square selected initially
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // sq_size
                row = location[1] // sq_size

                if sqSelected == (row, col):  # Deselect if same square
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                if len(playerClicks) == 2:
                    move = Chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessMove())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs, sqSelected)
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

if __name__ == "__main__":
    main()
