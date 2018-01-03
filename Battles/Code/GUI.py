"""
~~~~~~
GUI.py
~~~~~~

By - JATIN KUMAR MANDAV


A small library for Button widget for the game
This is completely coded using PYGAME library of PYTHON 2.7

Lines - 136

"""

# Imports
import pygame
import sys

# Initialize Pygame
pygame.init()

width = 0
height = 0
display = None

# Initialize display, width, margin, and height of pygame window
def initGUI(screen, size):
    global display, width, height
    display = screen
    width = size[0]
    height = size[1]

# Button  Class
class Button:
    def __init__(self, x, y, w, h, color, activeColor, action=None, border=None, borderWidth = 2):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.activeColor = activeColor
        self.arg = 0
        self.borderWidth = borderWidth
        self.action = action
        
        if border:
            self.border = border
        else:
            self.border = color
            
        self.image = None
        self.imagePos = None

        self.text = None
        self.textPos = None
        self.align = "center"
        self.font = "Times New Roman"
        self.fontSize = 11
        self.fontColor = (0, 0, 0)

        self.image = None
        self.imagePos = None

    def select(self):
        if isActive(self.x, self.y, self.w, self.h) and self.action != None:
            self.action(self.arg)
        
    def draw(self, index=0):
        if index == self.arg:
            color = self.activeColor
        else:
            color = self.color
        pygame.draw.rect(display, color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(display, self.border, (self.x, self.y, self.w, self.h), self.borderWidth)
        if (self.text):
            display.blit(self.text, self.textPos)
        if not (self.image == None):
            display.blit(self.image, self.imagePos)
        
    def addImage(self, image, pos):
        size = image.get_size()
        self.image = image
        self.imagePos = (self.x + pos[0] - size[0]/2, self.y + pos[1] - size[1]/2)
        
    def addText(self, text, pos, size=25, font="Times New Roman", color=(0, 0 ,0), align="center"):
        self.font = font
        self.fontSize = size
        self.fontColor = color
        self.align = align
        font = pygame.font.SysFont(font, size)
            
        self.text = font.render(text, True, color)
        self.textPos = getRect(self.text)
        if align == "center":
            self.textPos.center = (self.x + self.w/2 + pos[0], self.y + self.h/2 + pos[1])
        else:
            self.textPos = (self.x + 10 + pos[0], self.y + pos[1])
        
    def updateText(self, text, pos):
        font = pygame.font.SysFont(self.font, self.fontSize)
        self.text = font.render(text, True, self.fontColor)
        self.textPos = getRect(self.text)
        if self.align == "center":
            self.textPos.center = (self.x + self.w/2 + pos[0], self.y + self.h/2 + pos[1])
        else:
            self.textPos = (self.x + 10 + pos[0], self.y + pos[1])


def getRect(font):
    return font.get_rect()

# Check if mouse is over the button
def isActive(x, y, w, h):
    pos = pygame.mouse.get_pos()
    if (x < pos[0] < x + w) and (y < pos[1] < y + h):
        return True
    return False


if __name__ == "__main__":
    screen = pygame.display.set_mode((200, 100))
    initGUI(screen, (200, 100))
    newButton = Button(50, 25, 100, 50, (255, 255, 255))
    newButton.addText("Text", (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        display.fill(0)
        newButton.draw()
        pygame.display.update()
