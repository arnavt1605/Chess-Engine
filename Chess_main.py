#This is the main driver file responsible for user input and display the current state of game

import pygame as p
import Chess_engine

width = height =512
dimension = 8 
sq_size= height//dimension
max_fps=15   #for the animations later on
images={}


def loadImages():
    pieces= ['bR','bN','bB','bQ','bK','bp','wR','wN','wB','wQ','wK','wp']
    for piece in pieces:
        images[piece]=p.image.load("images/"+piece+".png")

def main():
    screen= p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs= Chess_engine.GameState()
    loadImages()
    running=True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False
        drawGameState(screen,gs)
        clock.tick(max_fps)
        p.display.flip()
    drawPieces(screen,board)


def drawGameState(screen,gs):
    drawBoard(screen)   #draws the squares on the board
    drawPieces(screen,gs.board)   #draws the pieces on the squares


def drawBoard(screen):
    colors=[p.Color("white"), p.Color("gray")]   #two colors of the chessboard
    for r in range(dimension):         #traversing the rows
        for c in range(dimension):   #travesring the columns
            color=colors[((r+c)%2)]    #very nice logic
            p.draw.rect(screen,color, p.Rect(r*sq_size , c*sq_size , sq_size , sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece= board[r][c]
            if piece !="--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
if __name__=="__main__":
    main()

