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

    sqSelected=()
    playerClicks=[]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running=False

            elif e.type == p.MOUSEBUTTONDOWN:
                location= p.mouse.get_pos()   #The location of the mouse at a particular instant
                col= location[0]//sq_size
                row= location[1]//sq_size
                if sqSelected == (row,col):    #If user clicks the same square once again 
                    sqSelected=()
                    playerClicks=[]

                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)    #Storing the user's moves as a list of tuples 

                if len(playerClicks)==2:
                    move= Chess_engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessMove())
                    gs. makeMove(move)
                    sqSelected= ()
                    playerClicks= []  #resetting the moves so that we can run the loop again and again.

                    
        drawGameState(screen,gs)
        clock.tick(max_fps)
        p.display.flip()
    drawPieces(screen,gs.board)


def drawGameState(screen,gs):
    drawBoard(screen)   #draws the squares on the board
    drawPieces(screen,gs.board)   #draws the pieces on the squares


def drawBoard(screen):
    colors=[p.Color("white"), p.Color("gray")]   #two colors of the chessboard
    for r in range(dimension):         #traversing the rows
        for c in range(dimension):   #traversing the columns
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

