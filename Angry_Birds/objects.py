'''

    Game: Angry Birds
    File: objects.py

    Contents: Class SLAB or WALL

    Requirements: Pygame, sys, math
    Supporting Modules: physics_engine

    By: Jatin Kumar Mandav

    Blog: https://www.jatinmandav.wordpress.com
    Twitter: @jatinmandav
    YouTube: https://www.youtube.com/mandav

'''
import pygame
import sys
from math import *

import physics_engine

pygame.init()
display = None
width = None
height = None
clock = pygame.time.Clock()
ground = 50

def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground

class Slab:
    def __init__(self, x, y, w, h, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        if self.w > self.h:
            self.image = pygame.image.load("Images/wall_horizontal.png")
        else:
            self.image = pygame.image.load("Images/wall_vertical.png")

        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        self.color = color

    def draw(self):
        display.blit(self.image, (self.x, self.y))

    def collision_manager(self, ball, type="BALL"):
        if type == "BALL":
            if (ball.y + ball.r > self.y) and (ball.y < self.y + self.h):
                if (ball.x < self.x + self.w) and (ball.x + ball.r > self.x + self.w):
                    ball.x = 2*(self.x + self.w) - ball.x
                    ball.velocity.angle = - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
                elif ball.x + ball.r > self.x and (ball.x < self.x):
                    ball.x = 2*(self.x - ball.r) - ball.x
                    ball.velocity.angle = - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
            if (ball.x + ball.r > self.x) and (ball.x < self.x + self.w):
                if ball.y + ball.r > self.y and ball.y < self.y:
                    ball.y = 2*(self.y - ball.r) - ball.y
                    ball.velocity.angle = pi - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity
                elif (ball.y < self.y + self.h) and (ball.y + ball.r > self.y + self.h):
                    ball.y = 2*(self.y + self.h) - ball.y
                    ball.velocity.angle = pi - ball.velocity.angle
                    ball.velocity.magnitude *= physics_engine.elasticity

            return ball
        else:
            block = ball
            if (block.y + block.h > self.y) and (block.y < self.y + self.h):
                if (block.x < self.x + self.w) and (block.x + block.w > self.x + self.w):
                    block.x = 2*(self.x + self.w) - block.x
                    block.velocity.angle = - block.velocity.angle
                    block.rotateAngle =  - block.velocity.angle
                    block.velocity.magnitude *= physics_engine.elasticity
                elif block.x + block.w > self.x and (block.x < self.x):
                    block.x = 2*(self.x - block.w) - block.x
                    block.velocity.angle = - block.velocity.angle
                    block.rotateAngle =  - block.velocity.angle
                    block.velocity.magnitude *= physics_engine.elasticity
            if (block.x + block.w > self.x) and (block.x < self.x + self.w):
                if block.y + block.h > self.y and block.y < self.y:
                    block.y = 2*(self.y - block.h) - block.y
                    block.velocity.angle = pi - block.velocity.angle
                    block.rotateAngle =  pi - block.velocity.angle
                    block.velocity.magnitude *= physics_engine.elasticity
                elif (block.y < self.y + self.h) and (block.y + block.h > self.y + self.h):
                    block.y = 2*(self.y + self.h) - block.y
                    block.velocity.angle = pi - block.velocity.angle
                    block.rotateAngle =  pi - block.velocity.angle
                    block.velocity.magnitude *= physics_engine.elasticity

            return block
