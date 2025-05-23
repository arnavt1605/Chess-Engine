import pygame as p
import Chess_engine

# Layout settings
BOARD_SIZE = 512
PANEL_WIDTH = 250
WINDOW_WIDTH = BOARD_SIZE + 2 * PANEL_WIDTH
WINDOW_HEIGHT = BOARD_SIZE
SQUARE_SIZE = BOARD_SIZE // 8
CAPTURE_ICON_SIZE = 32
MOVE_FONT_SIZE = 20
MAX_MOVES_SHOWN = 18

images = {}
small_images = {}

def loadImages():
    global images, small_images
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
    for piece in pieces:
        images[piece] = p.transform.smoothscale(
            p.image.load("images/" + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
        small_images[piece] = p.transform.smoothscale(
            images[piece], (CAPTURE_ICON_SIZE, CAPTURE_ICON_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = p.time.Clock()
    gs = Chess_engine.GameState()
    # Add captured piece tracking if not present
    if not hasattr(gs, "capturedWhite"):
        gs.capturedWhite = []
    if not hasattr(gs, "capturedBlack"):
        gs.capturedBlack = []
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    validMoves = gs.getValidMoves()
    moveMade = False

    # Board top-left
    board_x = PANEL_WIDTH
    board_y = 0

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                x, y = e.pos
                if board_x <= x < board_x + BOARD_SIZE and board_y <= y < board_y + BOARD_SIZE:
                    col = (x - board_x) // SQUARE_SIZE
                    row = (y - board_y) // SQUARE_SIZE
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

        screen.fill(p.Color("gainsboro"))
        drawSidePanel(screen, gs, left=True)
        drawSidePanel(screen, gs, left=False)
        drawGameState(screen, gs, sqSelected, board_x, board_y)
        clock.tick(60)
        p.display.flip()

def drawGameState(screen, gs, sqSelected, board_x, board_y):
    drawBoard(screen, board_x, board_y)
    highlightSquare(screen, sqSelected, board_x, board_y)
    drawPieces(screen, gs.board, board_x, board_y)

def drawBoard(screen, board_x, board_y):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[((r + c) % 2)]
            x = board_x + c * SQUARE_SIZE
            y = board_y + r * SQUARE_SIZE
            p.draw.rect(screen, color, p.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquare(screen, sqSelected, board_x, board_y):
    if sqSelected != ():
        s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        x = board_x + sqSelected[1] * SQUARE_SIZE
        y = board_y + sqSelected[0] * SQUARE_SIZE
        screen.blit(s, (x, y))

def drawPieces(screen, board, board_x, board_y):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                x = board_x + c * SQUARE_SIZE
                y = board_y + r * SQUARE_SIZE
                screen.blit(images[piece], p.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE))

def drawSidePanel(screen, gs, left=True):
    x0 = 0 if left else (WINDOW_WIDTH - PANEL_WIDTH)
    p.draw.rect(screen, p.Color("lightgray"), p.Rect(x0, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    font = p.font.SysFont("Arial", MOVE_FONT_SIZE, False, False)
    title_font = p.font.SysFont("Arial", MOVE_FONT_SIZE + 4, True)

    # Moves for this side
    moveLog = gs.moveLog
    moves = []
    if left:
        moves = [moveLog[i].getChessMove() for i in range(0, len(moveLog), 2)]
        captured = getattr(gs, 'capturedBlack', [])
        title = "White"
    else:
        moves = [moveLog[i].getChessMove() for i in range(1, len(moveLog), 2)]
        captured = getattr(gs, 'capturedWhite', [])
        title = "Black"

    # Draw player title
    text = title_font.render(title, True, p.Color("black"))
    screen.blit(text, (x0 + 20, 18))

    # Draw moves (bottom-up, most recent at bottom)
    n = min(MAX_MOVES_SHOWN, len(moves))
    for i in range(n):
        move_str = moves[-n + i]
        move_text = font.render(str(len(moves) - n + i + 1) + ". " + move_str, True, p.Color("black"))
        y = WINDOW_HEIGHT - 100 - (n - i) * (MOVE_FONT_SIZE + 4)
        screen.blit(move_text, (x0 + 18, y))

    # Draw captured pieces (icons) at the very bottom, left-to-right
    y_capt = WINDOW_HEIGHT - CAPTURE_ICON_SIZE - 20
    for i, piece in enumerate(captured[:8]):
        screen.blit(small_images[piece], (x0 + 18 + i * (CAPTURE_ICON_SIZE + 8), y_capt))

if __name__ == "__main__":
    main()
