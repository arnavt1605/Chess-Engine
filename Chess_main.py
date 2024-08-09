#This is the main driver file responsible for user input and display the current state of game

import pygame as p
from Chess import Chess_engine  #type: ignore

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


def drawGameState(screen,gs):
    drawBoard(screen)   #draws the squarees on the board
    drawPieces(screen,gs.board)   #draws the pieces on the squares


def drawBoard(screen):
    
if __name__ == "__main__":
    main()
