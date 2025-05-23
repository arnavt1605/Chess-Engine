import pygame as p
import Chess_engine

# Layout sizes
board_size = 512
panel_width = 160   # width for move/capture panels
panel_padding = 12
move_font_size = 18
capture_icon_size = 32
max_moves_shown = 16

width = board_size + 2 * panel_width
height = board_size

dimension = 8
sq_size = board_size // dimension
max_fps = 15
images = {}
small_images = {}

def loadImages():
    global images, small_images
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        images[piece] = p.image.load("images/" + piece + ".png")
        small_images[piece] = p.transform.scale(images[piece], (capture_icon_size, capture_icon_size))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
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
                x, y = e.pos
                # Only register clicks inside the chessboard
                if panel_width <= x < panel_width + board_size and y < board_size:
                    col = (x - panel_width) // sq_size
                    row = y // sq_size
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

        # Draw everything
        screen.fill(p.Color("gainsboro"))
        drawSidePanel(screen, gs, left=True)
        drawSidePanel(screen, gs, left=False)
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
            x = panel_width + c * sq_size
            y = r * sq_size
            p.draw.rect(screen, color, p.Rect(x, y, sq_size, sq_size))

def highlightSquare(screen, sqSelected):
    if sqSelected != ():
        s = p.Surface((sq_size, sq_size))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        x = panel_width + sqSelected[1] * sq_size
        y = sqSelected[0] * sq_size
        screen.blit(s, (x, y))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                x = panel_width + c * sq_size
                y = r * sq_size
                screen.blit(images[piece], p.Rect(x, y, sq_size, sq_size))

def drawSidePanel(screen, gs, left=True):
    # Panel background
    x0 = 0 if left else (panel_width + board_size)
    p.draw.rect(screen, p.Color("lightgray"), p.Rect(x0, 0, panel_width, height))

    font = p.font.SysFont("Arial", move_font_size, False, False)
    # Moves for this side
    moveLog = gs.moveLog
    moves = []
    if left:
        # White moves (even indices)
        moves = [moveLog[i].getChessMove() for i in range(0, len(moveLog), 2)]
        captured = gs.capturedBlack if hasattr(gs, 'capturedBlack') else []
        title = "White"
    else:
        # Black moves (odd indices)
        moves = [moveLog[i].getChessMove() for i in range(1, len(moveLog), 2)]
        captured = gs.capturedWhite if hasattr(gs, 'capturedWhite') else []
        title = "Black"

    # Draw player title
    title_font = p.font.SysFont("Arial", 22, True)
    title_text = title + " Moves"
    text = title_font.render(title_text, True, p.Color("black"))
    screen.blit(text, (x0 + panel_padding, panel_padding))

    # Draw moves (from bottom up, most recent at bottom)
    n = min(max_moves_shown, len(moves))
    for i in range(n):
        move_str = moves[-n + i]
        move_text = font.render(str(len(moves) - n + i + 1) + ". " + move_str, True, p.Color("black"))
        y = height - panel_padding - (n - i) * (move_font_size + 2) - capture_icon_size - 12
        screen.blit(move_text, (x0 + panel_padding, y))

    # Draw captured pieces (icons) at the very bottom, left-to-right
    y_capt = height - capture_icon_size - panel_padding
    for i, piece in enumerate(captured):
        screen.blit(small_images[piece], (x0 + panel_padding + i * (capture_icon_size + 4), y_capt))

if __name__ == "__main__":
    main()
