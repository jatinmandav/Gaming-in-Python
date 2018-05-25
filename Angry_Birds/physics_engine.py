'''

    Game: Angry Birds
    File: physics_engine.py

    Contents: Class Vector
              Class PIG
              Class BIRD
              Class BLOCK
              Class SLINGSHOT
              func collision_handler, block_collision_handler

    Requirements: Pygame, sys, math, random

    By: Jatin Kumar Mandav

    Blog: https://www.jatinmandav.wordpress.com
    Twitter: @jatinmandav
    YouTube: https://www.youtube.com/mandav

'''
import pygame
import sys
from math import *
import random

pygame.init()
width = None
height = None
display = None
ground = 50
clock = pygame.time.Clock()

def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground

class Vector:
    def __init__(self, magnitude=0, angle=radians(0)):
        self.magnitude = magnitude
        self.angle = angle

def add_vectors(vector1, vector2):
    x = sin(vector1.angle)*vector1.magnitude + sin(vector2.angle)*vector2.magnitude
    y = cos(vector1.angle)*vector1.magnitude + cos(vector2.angle)*vector2.magnitude

    new_angle = 0.5*pi - atan2(y, x)
    new_magnitude = hypot(x, y)

    new_vector = Vector(new_magnitude, new_angle)
    return new_vector

gravity = Vector(0.2, pi)
inverse_friction = 0.99
elasticity = 0.8
block_elasticity = 0.7

class Pig:
    def __init__(self, x, y, r, v=None, type="PIG", loaded = False, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.r = r
        if v == None:
            self.velocity = Vector()
        else:
            self.velocity = v

        self.pig1_image = pygame.image.load("Images/pig1.png")
        self.pig2_image = pygame.image.load("Images/pig3.png")

        self.pig_dead = pygame.image.load("Images/pig_damaged.png")

        self.bird_image = pygame.image.load("Images/bird.png")

        if type == "PIG":
            self.image = random.choice([self.pig1_image, self.pig2_image])
        else:
            self.image = self.bird_image

        self.type = type
        self.color = color
        self.loaded = loaded
        self.path = []
        self.count = 0
        self.animate_count = 0
        self.isDead = False

    def draw(self):
        self.animate_count += 1

        if self.type == "BIRD" and not self.loaded:
            for point in self.path:
                pygame.draw.ellipse(display, self.color, (point[0], point[1], 3, 3), 1)

        if (self.type == "PIG") and (not self.animate_count%20) and (not self.isDead):
            self.image = random.choice([self.pig1_image, self.pig2_image])

        display.blit(self.image, (self.x - self.r, self.y - self.r))


    def dead(self):
        self.isDead = True
        self.image = self.pig_dead

    def move(self):
        self.velocity = add_vectors(self.velocity, gravity)

        self.x += self.velocity.magnitude*sin(self.velocity.angle)
        self.y -= self.velocity.magnitude*cos(self.velocity.angle)

        self.velocity.magnitude *= inverse_friction

        if self.x > width - self.r:
            self.x = 2*(width - self.r) - self.x
            self.velocity.angle *= -1
            self.velocity.magnitude *= elasticity
        elif self.x < self.r:
            self.x = 2*self.r - self.x
            self.velocity.angle *= -1
            self.velocity.magnitude *= elasticity

        if self.y > height - self.r:
            self.y = 2*(height - self.r) - self.y
            self.velocity.angle = pi - self.velocity.angle
            self.velocity.magnitude *= elasticity
        elif self.y < self.r:
            self.y = 2*self.r - self.y
            self.velocity.angle = pi - self.velocity.angle
            self.velocity.magnitude *= elasticity

        self.count += 1
        if self.count%1 == 0:
            self.path.append((self.x, self.y))

class Bird(Pig):
    def load(self, slingshot):
        self.x = slingshot.x
        self.y = slingshot.y
        self.loaded = True

    def mouse_selected(self):
        pos = pygame.mouse.get_pos()
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        dist = hypot(dy, dx)
        if dist < self.r:
            return True

        return False

    def reposition(self, slingshot, mouse_click):
        pos = pygame.mouse.get_pos()
        if self.mouse_selected():
            self.x = pos[0]
            self.y = pos[1]

            dx = slingshot.x - self.x
            dy = slingshot.y - self.y
            self.velocity.magnitude = int(hypot(dx, dy)/2)
            if self.velocity.magnitude > 80:
                self.velocity.magnitude = 80
            self.velocity.angle = pi/2 + atan2(dy, dx)

    def unload(self):
        self.loaded = False

    def project_path(self):
        if self.loaded:
            path = []
            ball = Pig(self.x, self.y, self.r, self.velocity, self.type)
            for i in range(30):
                ball.move()
                if i%5 == 0:
                    path.append((ball.x, ball.y))

            for point in path:
                pygame.draw.ellipse(display, self.color, (point[0], point[1], 2, 2))


class Block:
    def __init__(self, x, y, r, v=None, color=( 120, 40, 31 ), colorBoundary = ( 28, 40, 51 )):
        self.r = 50
        self.w = 100
        self.h = 100

        self.x = x
        self.y = y

        self.block_image = pygame.image.load("Images/block1.png")
        self.block_destroyed_image = pygame.image.load("Images/block_destroyed1.png")

        self.image = self.block_image

        if v == None:
            self.velocity = Vector()
        else:
            self.velocity = v

        self.color = color
        self.colorDestroyed = ( 100, 30, 22 )
        self.colorBoundary = colorBoundary
        self.rotateAngle = radians(0)
        self.anchor = (self.r/2, self.r/2)

        self.isDestroyed = False

    def rotate(self, coord, angle, anchor=(0, 0)):
        corr = 0
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]

    def draw(self):
        pygame.transform.rotate(self.image, self.rotateAngle)
        display.blit(self.image, (self.x - self.w/2, self.y))

    def destroy(self):
        self.isDestroyed = True
        self.image = self.block_destroyed_image

    def move(self):
        self.velocity = add_vectors(self.velocity, gravity)

        self.x += self.velocity.magnitude*sin(self.velocity.angle)
        self.y -= self.velocity.magnitude*cos(self.velocity.angle)

        self.velocity.magnitude *= inverse_friction

        if self.x > width - self.w:
            self.x = 2*(width - self.w) - self.x
            self.velocity.angle *= -1
            self.rotateAngle = - self.velocity.angle
            self.velocity.magnitude *= block_elasticity
        elif self.x < self.w:
            self.x = 2*self.w - self.x
            self.velocity.angle *= -1
            self.rotateAngle = - self.velocity.angle
            self.velocity.magnitude *= block_elasticity

        if self.y > height - self.h:
            self.y = 2*(height - self.h) - self.y
            self.velocity.angle = pi - self.velocity.angle
            self.rotateAngle = pi - self.velocity.angle
            self.velocity.magnitude *= block_elasticity
        elif self.y < self.h:
            self.y = 2*self.h - self.y
            self.velocity.angle = pi - self.velocity.angle
            self.rotateAngle = pi - self.velocity.angle
            self.velocity.magnitude *= block_elasticity


class Slingshot:
    def __init__(self, x, y, w, h, color=( 66, 73, 73 )):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def rotate(self, coord, angle, anchor=(0, 0)):
        corr = 0
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]

    def draw(self, loaded=None):
        pygame.draw.rect(display, self.color, (self.x, self.y + self.h*1/3, self.w, self.h*2/3))

        if (not loaded == None) and loaded.loaded:
            pygame.draw.line(display, ( 100, 30, 22 ), (self.x - self.w/4 + self.w/4, self.y + self.h/6), (loaded.x, loaded.y + loaded.r/2), 10)
            pygame.draw.line(display, ( 100, 30, 22 ), (self.x + self.w, self.y + self.h/6), (loaded.x + loaded.r, loaded.y + loaded.r/2), 10)

        pygame.draw.rect(display, self.color, (self.x - self.w/4, self.y, self.w/2, self.h/3), 5)
        pygame.draw.rect(display, self.color, (self.x + self.w - self.w/4, self.y, self.w/2, self.h/3), 5)

def collision_handler(b_1, b_2, type):
    collision = False
    if type == "BALL":
        dx = b_1.x - b_2.x
        dy = b_1.y - b_2.y

        dist = hypot(dx, dy)
        if dist < b_1.r + b_2.r:
            tangent = atan2(dy, dx)
            angle = 0.5*pi + tangent

            angle1 = 2*tangent - b_1.velocity.angle
            angle2 = 2*tangent - b_2.velocity.angle

            magnitude1 = b_2.velocity.magnitude
            magnitude2 = b_1.velocity.magnitude

            b_1.velocity = Vector(magnitude1, angle1)
            b_2.velocity = Vector(magnitude2, angle2)

            b_1.velocity.magnitude *= elasticity
            b_2.velocity.magnitude *= elasticity

            overlap = 0.5*(b_1.r + b_2.r - dist + 1)
            b_1.x += sin(angle)*overlap
            b_1.y -= cos(angle)*overlap
            b_2.x -= sin(angle)*overlap
            b_2.y += cos(angle)*overlap
            collision = True
            #print(collision)

        #print(collision)
        return b_1, b_2, collision
    elif type == "BALL_N_BLOCK":
        dx = b_1.x - b_2.x
        dy = b_1.y - b_2.y

        dist = hypot(dx, dy)
        if dist < b_1.r + b_2.w:
            tangent = atan2(dy, dx)
            angle = 0.5*pi + tangent

            angle1 = 2*tangent - b_1.velocity.angle
            angle2 = 2*tangent - b_2.velocity.angle

            magnitude1 = b_2.velocity.magnitude
            magnitude2 = b_1.velocity.magnitude

            b_1.velocity = Vector(magnitude1, angle1)
            b_2.velocity = Vector(magnitude2, angle2)

            b_1.velocity.magnitude *= elasticity
            b_2.velocity.magnitude *= block_elasticity

            overlap = 0.5*(b_1.r + b_2.w - dist + 1)
            b_1.x += sin(angle)*overlap
            b_1.y -= cos(angle)*overlap
            b_2.x -= sin(angle)*overlap
            b_2.y += cos(angle)*overlap
            collision = True

        return b_1, b_2, collision

def block_collision_handler(block, block2):
    collision = False
    if (block.y + block.h > block2.y) and (block.y < block2.y + block2.h):
        if (block.x < block2.x + block2.w) and (block.x + block.w > block2.x + block2.w):
            block.x = 2*(block2.x + block2.w) - block.x
            block.velocity.angle = - block.velocity.angle
            block.rotateAngle = - block.velocity.angle
            block.velocity.magnitude *= block_elasticity

            block2.velocity.angle = - block2.velocity.angle
            block2.rotateAngle = - block2.velocity.angle
            block2.velocity.magnitude *= block_elasticity
            collision = True

        elif block.x + block.w > block2.x and (block.x < block2.x):
            block.x = 2*(block2.x - block.w) - block.x
            block.velocity.angle = - block.velocity.angle
            block.rotateAngle = - block.velocity.angle
            block.velocity.magnitude *= block_elasticity

            block2.velocity.angle = - block2.velocity.angle
            block2.rotateAngle = - block2.velocity.angle
            block2.velocity.magnitude *= block_elasticity
            collision = True

    if (block.x + block.w > block2.x) and (block.x < block2.x + block2.w):
        if block.y + block.h > block2.y and block.y < block2.y:
            block.y = 2*(block2.y - block.h) - block.y
            block.velocity.angle = pi - block.velocity.angle
            block.rotateAngle = pi - block.velocity.angle
            block.velocity.magnitude *= block_elasticity

            block2.velocity.angle = pi - block2.velocity.angle
            block2.rotateAngle = pi - block2.velocity.angle
            block2.velocity.magnitude *= block_elasticity
            collision = True

        elif (block.y < block2.y + block2.h) and (block.y + block.h > block2.y + block2.h):
            block.y = 2*(block2.y + block2.h) - block.y
            block.velocity.angle = pi - block.velocity.angle
            block.rotateAngle = pi - block.velocity.angle
            block.velocity.magnitude *= block_elasticity

            block2.velocity.angle = pi - block2.velocity.angle
            block2.rotateAngle = pi - block2.velocity.angle
            block2.velocity.magnitude *= block_elasticity
            collision = True

    return block, block2, collision
