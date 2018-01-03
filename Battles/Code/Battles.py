"""
~~~~~~~~~~~~~~
Battles.py
~~~~~~~~~~~~~~

By - JATIN KUMAR MANDAV

BATTLES is inspired by mobile strategy video game Clash of Clans
which is developed and published by Finnish game developer Supercell.

This game is developed using PYGAME library of PYTHON 2.7

Lines - 127

"""

import pygame
import sys
from math import *
from GUI import *
from Maps import *
from Structures import *

pygame.init()

width = 1260
height = 720

margin = 25

groundW = width - 150 - 2*margin
groundH = height - 2*margin

display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()

initGUI(display, (width, height))
initStruct(display, (groundW, groundH), margin)
initMaps(display, (width, height), margin, 100)


white = (255, 255, 255)
black = (0, 0, 0)
yellow = (241, 196, 15)
red = (203, 67, 53)
green = (30, 132, 73)
blue = (36, 113, 163)
gray = (113, 125, 126)

activeButton = 0


def drawBorder():
    pygame.draw.rect(display, black, (margin, margin, groundW, groundH), 2)

def createMaps(arg=0):
    maps = Maps()
    maps.createMap()

def adventure(arg=0):
    maps = Maps()
    maps.openMap([0, "adventure"])

def customMap(arg=0):
    maps = Maps()
    maps.openMap([0, "custom"])

def close(arg=0):
    pygame.quit()
    sys.exit()

def game():
    loop = True
    font = pygame.font.SysFont("Agency FB", 50)
    font.set_bold(True)
    mandav = font.render("MANDAV", True, (71, 71, 71))
    
    font2 = pygame.font.SysFont("Agency FB", 200)
    font2.set_bold(True)
    title = font2.render("BATTLES", True, (200, 200, 200))
    titlePos = title.get_rect()
    titlePos.center = [width/2, height/2 - 200]

    tank = pygame.image.load("Images/Tank.png")
    tankPos = tank.get_rect()
    tankPos.center = [width/2, height/2 + 40]

    heli = pygame.image.load("Images/Helicopter.png")
    heliPos = heli.get_rect()
    heliPos.center = [width/2 - 70, height/2 - 100]

    quit = Button(width - 300 - 10, height/2 + 200, 300, 100, blue, blue, close)
    quit.addText("QUIT", (0, 0), 30, "Showcard Gothic", (150, 150, 150))
    
    create = Button(width - 600 - 20, height/2 + 200, 300, 100, blue, blue, createMaps)
    create.addText("CREATE MAPS", (0, 0), 30, "Showcard Gothic", (150, 150, 150))
    
    adven = Button(width - 900 - 30, height/2 + 200, 300, 100, blue, blue, adventure)
    adven.addText("ADVENTURE", (0, 0), 30, "Showcard Gothic", (150, 150, 150))
    
    custom = Button(width - 1200 - 40, height/2 + 200, 300, 100, blue, blue, customMap)
    custom.addText("CUSTOM BASES", (0, 0), 30, "Showcard Gothic", (150, 150, 150))
    
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
            if event.type == pygame.MOUSEBUTTONDOWN:
                quit.select()
                create.select()
                adven.select()
                custom.select()
                
        display.fill((51,51,51))

        display.blit(title, titlePos)
        display.blit(heli, heliPos)
        display.blit(tank, tankPos)

        display.blit(mandav, (width - 200, height - 60))

        quit.draw()
        create.draw()
        adven.draw()
        custom.draw()
        
        pygame.display.update()
        clock.tick(60)

game()
