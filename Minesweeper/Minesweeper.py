# -----------------------------------------------------------------------------
#
# Minesweeper
# Language - Python
# Modules - pygame, sys, random
#
# Controls - Single Mouse Click on any box, r to reset the grid
#
# By - Jatin Kumar Mandav
#
# Website - https://jatinmandav.wordpress.com
#
# YouTube Channel - https://www.youtube.com/channel/UCdpf6Lz3V357cIZomPwjuFQ
# Twitter - @jatinmandav
#
# -----------------------------------------------------------------------------

import pygame
import sys
import random

pygame.init()

width = 510
height = 510
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

background = (51, 51, 51)
white = (236, 240, 241)
darkWhite = (174, 182, 191)
gray = (52, 73, 94)
yellow = (244, 208, 63)
lightred = (236, 112, 99)

grid = []
size = 10
mineProb = 30

safeSpots = 0
revealedSpots = 0

numberFont = pygame.font.SysFont("Times New Roman", width/(size*2))
font = pygame.font.SysFont("Times New Roman", 35)

# Property of Each Cell on Grid
class Spot:
    def __init__(self, x, y, w, h, mineState):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.isMine = mineState
        self.neighbors = 0
        self.reveal = False

    # Draw Cells
    def draw(self):
        if not self.reveal:
            pygame.draw.rect(display, white, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, darkWhite, (self.x, self.y, self.w, self.h))

        if self.reveal:
            if self.isMine:
                pygame.draw.ellipse(display, gray, (self.x + self.w/4, self.y + self.h/4, self.w/2, self.h/2))
            else:
                if not self.neighbors == 0:
                    num = numberFont.render(str(self.neighbors), True, gray)
                    display.blit(num, (self.x + self.w/4, self.y + self.h/4))

    # Check if the Cell is a Mine and reveal others if Block has no Mine Surrounding
    def checkForMine(self, i, j):
        global revealedSpots
        self.reveal = True
        revealedSpots += 1

        if self.isMine:
            for i in range(size):
                for j in range(size):
                    grid[i][j].reveal = True

            drawGrid()
            pygame.display.update()
            gameLost()
            
        elif grid[i][j].neighbors == 0:
            if i > 0:
                if not grid[i-1][j].isMine:
                    grid[i-1][j].reveal = True
                    revealedSpots += 1
            if j > 0:
                if not grid[i][j-1].isMine:
                    grid[i][j-1].reveal = True
                    revealedSpots += 1
            if i < size - 1:
                if not grid[i+1][j].isMine:
                    grid[i+1][j].reveal = True
                    revealedSpots += 1
            if j < size - 1:
                if not grid[i][j+1].isMine:
                    grid[i][j+1].reveal = True
                    revealedSpots += 1
            if i > 0 and j > 0:
                if not grid[i-1][j-1].isMine:
                    grid[i-1][j-1].reveal = True
                    revealedSpots += 1
            if i > 0 and  j < size - 1:
                if not grid[i-1][j+1].isMine:
                    grid[i-1][j+1].reveal = True
                    revealedSpots += 1
            if i < size - 1 and j > 0:
                if not grid[i+1][j-1].isMine:
                    grid[i+1][j-1].reveal = True
                    revealedSpots += 1
            if i < size - 1 and j < size - 1:
                if not grid[i+1][j+1].isMine:
                    grid[i+1][j+1].reveal = True
                    revealedSpots += 1

    # Count Neighboring Mines
    def countNeighborMines(self, i, j):
        if not self.isMine:
            if i > 0:
                if grid[i-1][j].isMine:
                    self.neighbors += 1
            if j > 0:
                if grid[i][j-1].isMine:
                    self.neighbors += 1  
            if i < size - 1:
                if grid[i+1][j].isMine:
                    self.neighbors += 1
            if j < size - 1:
                if grid[i][j+1].isMine:
                    self.neighbors += 1
            if i > 0 and j > 0:
                if grid[i-1][j-1].isMine:
                    self.neighbors += 1
            if i > 0 and  j < size - 1:
                if grid[i-1][j+1].isMine:
                    self.neighbors += 1
            if i < size - 1 and j > 0:
                if grid[i+1][j-1].isMine:
                    self.neighbors += 1
            if i < size - 1 and j < size - 1:
                if grid[i+1][j+1].isMine:
                    self.neighbors += 1
        

# Initialize the Grid             
def generateGrid():
    global grid, safeSpots
    grid = []
    for i in range(size):
        grid.append([])
        for j in range(size):
            prob = random.randint(1, 100)
            if prob < mineProb:
                newObj = Spot((width/size)*(j), (height/size)*(i), width/size - 3, height/size - 3, True)
            else:
                safeSpots += 1
                newObj = Spot((width/size)*(j), (height/size)*(i), width/size - 3, height/size - 3, False)
                
            grid[i].append(newObj)

    for i in range(size):
        for j in range(size):
            grid[i][j].countNeighborMines(i, j)

# Check if Grid is solved
def gameWon():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    reset()
                    
        font.set_bold(True)
        text = font.render("You Won the Minesweeper!", True, yellow)
        display.blit(text, (width/2 - 250, height/2))
        pygame.display.update()
        clock.tick(60)

# Check if Game is Lost        
def gameLost():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    reset()
                    
        font.set_bold(True)
        text = font.render("You Lost the Game!", True, (236, 112, 99))
        display.blit(text, (width/2 - 250, height/2))
        pygame.display.update()
        clock.tick(60)

# Draw the Grid
def drawGrid():
    for i in range(size):
        for j in range(size):
            grid[i][j].draw()

# Reset the Grid
def reset():
    minesweeper()

# Close the Game
def close():
    pygame.quit()
    sys.exit()

# The Game
def minesweeper():
    loop = True

    generateGrid()
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_r:
                    reset()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                j = pos[0]/(width/size)
                i = pos[1]/(width/size)
                grid[i][j].checkForMine(i, j)

        display.fill(background)

        drawGrid()

        if revealedSpots == safeSpots:
            gameWon()
        
        pygame.display.update()
        clock.tick(60)

minesweeper()
