'''

    Game: Angry Birds
    File: interface.py

    Contents: Class Buttons and Class Labels for User Interface

    Requirements: Pygame, sys

    By: Jatin Kumar Mandav

    Blog: https://www.jatinmandav.wordpress.com
    Twitter: @jatinmandav
    YouTube: https://www.youtube.com/mandav

'''
import pygame
import sys

pygame.init()
display = None

def init(screen):
    global display
    display = screen

class Button:
    def __init__(self, x, y, w, h, action=None, colorNotActive=(189, 195, 199), colorActive=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.colorActive = colorActive
        self.colorNotActive = colorNotActive

        self.action = action

        self.font = None
        self.text = None
        self.text_pos = None

    def add_text(self, text, size=20, font="Times New Roman", text_color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, text_color)
        self.text_pos = self.text.get_rect()

        self.text_pos.center = (self.x + self.w/2, self.y + self.h/2)

    def draw(self):
        if self.isActive():
            if not self.colorActive == None:
                pygame.draw.rect(display, self.colorActive, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.colorNotActive, (self.x, self.y, self.w, self.h))

        if self.text:
            display.blit(self.text, self.text_pos)

    def isActive(self):
        pos = pygame.mouse.get_pos()

        if (self.x < pos[0] < self.x + self.w) and (self.y < pos[1] < self.y + self.h):
            return True
        else:
            return False

class Label(Button):
    def draw(self):
        if self.text:
            display.blit(self.text, self.text_pos)
