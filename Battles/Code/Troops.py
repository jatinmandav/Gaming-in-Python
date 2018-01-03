"""
~~~~~~~~~
Troops.py
~~~~~~~~~

By - JATIN KUMAR MANDAV

This library contains different Troops classes for the game
Troops: 1. SHOOTERS
        2. TANKS
        3. HELICOPTERS

Also contains funcions to draw different shapes

This is completely coded in using PYGAME library of PYTHON 2.7

Lines - 777

"""

# Imports

import pygame
import sys
from math import *

# Initialize PyGame
pygame.init()

margin = 0
width = 400
height = 400
display = None

def initTroops(screen, size, m):
    global display, width, height, margin
    display = screen
    width = size[0]
    height = size[1]
    margin = m
    

def getCoordPoly(x, y, r, n, rotate=0, anchor=(0, 0)):
    coords = []
    for i in range(n):
        coords.append([x - anchor[0] + r*cos(2*pi*i/n + rotate), y - anchor[1] + r*sin(2*pi*i/n + rotate)])

    #pygame.draw.polygon(display, black, coords, 1)

    return coords[:]

class Shots:
    def __init__(self, x, y, r1, speed, angle, color=(0, 0, 0), type="circle", r2=0):
        self.x = x
        self.y = y
        self.r1 = r1
        if r2 == 0:
            self.r2 = r1
        else:
            self.r2 = r2

        self.type = type
         
        self.speed = speed
        self.angle = angle
        self.color = color
        
    def draw(self):
        if self.type == "circle":
            pygame.draw.ellipse(display, self.color, (self.x - self.r1, self.y - self.r2, self.r1*2, self.r2*2))
        elif self.type == "line":
            x2 = self.x + self.r1*cos(self.angle)
            y2 = self.y + self.r1*sin(self.angle)
            pygame.draw.line(display, self.color, (self.x, self.y), (x2, y2), 2)
            
    def move(self):
        self.x += self.speed*cos(self.angle)
        self.y += self.speed*sin(self.angle)


class Shooter:
    def __init__(self, x, y, r, speed, range, level, shotSpeed, radius):
        self.x = x
        self.y = y

        self.range = range
        self.shotSpeed = shotSpeed
        self.radius = radius
        
        self.r = r
        self.speed = speed
        self.speedMemory = speed
        self.level = level

        self.slow = 20

        if self.level == 1:
            self.colorBase = (125, 102, 8)
            self.colorHead = (212, 172, 13)
            self.colorGun = (40, 55, 71)
            self.hitPoint = 45
            self.health = self.hitPoint
            self.damage = 8
        elif self.level == 2:
            self.colorBase = (19, 141, 117)
            self.colorHead = (11, 83, 69)
            self.colorGun = (52, 73, 94)
            self.hitPoint = 60
            self.health = self.hitPoint
            self.damage = 14
        elif self.level == 3:
            self.colorBase = (46, 134, 193)
            self.colorHead = (21, 67, 96)
            self.colorGun = (33, 47, 60)
            self.hitPoint = 80
            self.health = self.hitPoint
            self.damage = 23
        elif self.level == 4:
            self.colorBase = (26, 82, 118)
            self.colorHead = (20, 143, 119)
            self.colorGun = (23, 32, 42)
            self.hitPoint = 100
            self.health = self.hitPoint
            self.damage = 25
            self.slow = 30
        elif self.level == 5:
            self.colorBase = (69, 179, 157)
            self.colorHead = (244, 208, 63)
            self.colorGun = (23, 32, 42)
            self.hitPoint = 120
            self.health = self.hitPoint
            self.damage = 35
            self.slow = 30

        self.angle = 0
        self.delay = 0
        
        self.gunCoord = []
        self.gunCoord2 = []
        self.shots = []

        self.nearestPos = None
        
        self.type = "GROUND"

        self.font = pygame.font.SysFont("Agency FB", 15)

    def updateHealth(self, defenceStruct):
        error = self.r
        for struct in defenceStruct:
            if not (struct.type == "HEADQUARTERS" or struct.type == "RESOURCE") and (struct.attackType == "GROUND" or struct.attackType == "GROUND AND AIR"):
                if (abs(struct.nearestPos[0] - self.x) < error)  and (abs(struct.nearestPos[1] - self.y) < error):
                    for shot in struct.shots:
                        if struct.isHit((shot.x, shot.y)):
                            self.health -= struct.damage
                            
    def isHit(self, coord):
        error = 30
        dist = ((self.nearestPos[0] - coord[0])**2 + (self.nearestPos[1] - coord[1])**2)**0.5
        if dist < error:
            return True
        return False

    def removeHit(self):
        tempList = self.shots[:]
        for shot in self.shots:
            if self.isHit((shot.x, shot.y)):
                tempList.remove(shot)

        self.shots = tempList[:]
                
    def shoot(self):
        self.delay = (self.delay + 1)%100
        if self.delay%self.slow == 0:
            pos = self.nearestPos
            dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
            self.angle = atan2(pos[1] - self.y, pos[0] - self.x)
            
            if dist < self.range/2:
                shot = Shots((self.gunCoord[1][0] + self.gunCoord[2][0])/2, (self.gunCoord[1][1] + self.gunCoord[2][1])/2, self.radius, self.shotSpeed, self.angle)
                self.shots.append(shot)
                if self.level >= 4:
                    shot = Shots((self.gunCoord2[1][0] + self.gunCoord2[2][0])/2, (self.gunCoord2[1][1] + self.gunCoord2[2][1])/2, self.radius, self.shotSpeed, self.angle)
                    self.shots.append(shot)
        tempList = self.shots[:]
                
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    
    def rotate(self, coord, angle, anchor=(0, 0), corr=270):
        corr = corr
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]

    def draw(self):
        w = self.r*4/5
        h = self.r*4
        #pos = pygame.mouse.get_pos()
        pos = self.nearestPos
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)
        
        rectCoord = [(0, 0), (0, h), (w, h), (w, 0)]

        baseCoord = []
        
        for point in rectCoord:
            baseCoord.append(self.translate(self.rotate(point, rotate, (w/2, h/2), 180)))

        w = self.r/2
        h = self.r*2
        
        rectCoord = [(0, 0), (0, h), (w, h), (w, 0)]

        self.gunCoord = []
        shift = w/2
        if self.level >= 4:
            shift = 2*w
            self.gunCoord2 = []
            for point in rectCoord:
                self.gunCoord2.append(self.translate(self.rotate(point, rotate, (-2*w, 0), 270)))
        for point in rectCoord:
            self.gunCoord.append(self.translate(self.rotate(point, rotate, (shift, 0), 270)))
        
        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r*5, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r*5 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))


        if self.level >= 4:
            pygame.draw.polygon(display, self.colorGun, self.gunCoord2)
        pygame.draw.polygon(display, self.colorGun, self.gunCoord)
        pygame.draw.polygon(display, self.colorBase, baseCoord)
        pygame.draw.ellipse(display, self.colorHead, (self.x - self.r, self.y - self.r, self.r*2, self.r*2))
        
        #pygame.draw.ellipse(display, (123, 125, 125), (self.x - self.range/2, self.y - self.range/2, self.range, self.range), 1)
                
    def move(self, defenceStruct):
        if len(defenceStruct):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in defenceStruct:
                dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                if lowestDist > dist:
                    self.nearestPos = [struct.x, struct.y]
                    lowestDist = dist
        else:
            self.nearestPos = pygame.mouse.get_pos()
        
        angle = atan2(self.nearestPos[1] - self.y, self.nearestPos[0] - self.x)
        self.x += self.speed*cos(angle)
        self.y += self.speed*sin(angle)
        dist = abs(self.nearestPos[1] - self.y) + abs(self.nearestPos[0] - self.x)
        if dist < self.range/2:
            self.speed = 0
        else:
            self.speed = self.speedMemory

class Tank:
    def __init__(self, x, y, r, speed, range, level, shotSpeed, radius):
        self.x = x
        self.y = y
        self.barrelX = x
        self.barrelY = y

        self.range = range
        self.shotSpeed = shotSpeed
        self.radius = radius
        
        self.r = r
        self.speed = speed
        self.speedMemory = speed

        self.level = level

        if self.level == 1:
            self.colorBase = (125, 102, 8)
            self.colorWheel = (11, 83, 69)
            self.colorGun = (14, 98, 81)
            self.colorHead = (20, 90, 50)
            self.hitPoint = 300
            self.damage = 5
        elif self.level == 2:
            self.colorBase = (19, 141, 117)
            self.colorWheel = (14, 98, 81)
            self.colorGun = (11, 83, 69)
            self.colorHead = (14, 98, 81)
            self.hitPoint = 430
            self.damage = 8
        elif self.level == 3:
            self.colorBase = (41, 128, 185)
            self.colorWheel = (21, 67, 96)
            self.colorGun = (36, 113, 163)
            self.colorHead = (21, 67, 96)
            self.hitPoint = 570
            self.damage = 12
        elif self.level == 4:
            self.colorBase = (52, 73, 94)
            self.colorWheel = (33, 47, 61)
            self.colorGun = (23, 32, 42)
            self.colorHead = (33, 47, 61)
            self.hitPoint = 730
            self.damage = 13
            self.gunCoord2 = []

        self.angle = 0
        self.health = self.hitPoint
        
        self.gunCoord = []
        self.shots = []

        self.type = "GROUND"

        self.nearestPos = None
        
        self.recoil = r/8
        self.rebound = 0.2 

        self.font = pygame.font.SysFont("Agency FB", 15)

    def updateHealth(self, defenceStruct):
        error = self.r
        for struct in defenceStruct:
            if (not (struct.type == "HEADQUARTERS" or struct.type == "RESOURCE")) and (struct.attackType == "GROUND" or struct.attackType == "GROUND AND AIR"):
                if (abs(struct.nearestPos[0] - self.x) < error)  and (abs(struct.nearestPos[1] - self.y) < error):
                    for shot in struct.shots:
                        if struct.isHit((shot.x, shot.y)):
                            self.health -= struct.damage
        
    def isHit(self, coord):
        error = self.r
        dist = ((self.nearestPos[0] - coord[0])**2 + (self.nearestPos[1] - coord[1])**2)**0.5
        if dist < error:
            return True
        return False

    def removeHit(self):
        tempList = self.shots[:]
        for shot in self.shots:
            if self.isHit((shot.x, shot.y)):
                tempList.remove(shot)

        self.shots = tempList[:]
                
    def shoot(self):
        error = 0.5

        if not ((abs(self.barrelX - self.x) < error) and (abs(self.barrelY - self.y) < error)):
            self.barrelX += self.rebound*cos(self.angle)
            self.barrelY += self.rebound*sin(self.angle)
        else:
            pos = self.nearestPos
            #pos = pygame.mouse.get_pos()
            dist = ((self.barrelX - pos[0])**2 + (self.barrelY - pos[1])**2)**0.5
            self.angle = atan2(pos[1] - self.barrelY, pos[0] - self.barrelX)
            
            if dist < self.range/2:
                shot = Shots((self.gunCoord[1][0] + self.gunCoord[2][0])/2, (self.gunCoord[1][1] + self.gunCoord[2][1])/2, self.radius, self.shotSpeed, self.angle)
                self.shots.append(shot)
                if self.level == 4:
                    shot = Shots((self.gunCoord2[1][0] + self.gunCoord2[2][0])/2, (self.gunCoord2[1][1] + self.gunCoord2[2][1])/2, self.radius, self.shotSpeed, self.angle)
                    self.shots.append(shot)
                self.barrelX -= self.recoil*cos(self.angle)
                self.barrelY -= self.recoil*sin(self.angle)

        tempList = self.shots[:]
                
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    
    def rotate(self, coord, angle, anchor=(0, 0), corr=270):
        corr = corr
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord, point=-1):
        if point == -1:
            return [coord[0] + self.x, coord[1] + self.y]
        else:
            return [coord[0] + point[0], coord[1] + point[1]]

    def draw(self):
        #pos = pygame.mouse.get_pos()
        pos = self.nearestPos
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)

        baseCoord = []
        w = self.r
        h = self.r*7/4
        base = [(0, 0), (0, h), (w, h), (w, 0)]
        for point in base:
            baseCoord.append(self.translate(self.rotate(point, rotate, (w/2, h/2))))        
        
        w = self.r/3
        h = self.r*2
        wheels = [(0, 0), (0, h), (w, h), (w, 0)]

        wheel1 = []
        wheel2 = []
        
        for point in wheels:
            wheel1.append(self.translate(self.rotate(point, rotate, (w/2 - self.r/2 - w/2, h/2))))
            wheel2.append(self.translate(self.rotate(point, rotate, (w/2 + self.r/2 + w/2, h/2))))

        sides = 5
        if self.level >= 3:
            sides = 8
        head = getCoordPoly(self.barrelX, self.barrelY , self.r/2, sides, rotate)

        w = self.r/4
        h = self.r*1.2
        coord = [(0, 0), (0, h), (w, h), (w, 0)]

        self.gunCoord = []
        self.gunCoord2 = []
        
        if self.level == 4:
            for point in coord:
                self.gunCoord.append(self.translate(self.rotate(point, rotate, (w/2 + w, 0)), (self.barrelX, self.barrelY)))
                self.gunCoord2.append(self.translate(self.rotate(point, rotate, (w/2 - w, 0)), (self.barrelX, self.barrelY)))
        else:
            for point in coord:
                self.gunCoord.append(self.translate(self.rotate(point, rotate, (w/2, 0)), (self.barrelX, self.barrelY)))

        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r*2, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r*2 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))
   
        pygame.draw.polygon(display, self.colorBase, baseCoord)
        pygame.draw.polygon(display, self.colorWheel, wheel1)
        pygame.draw.polygon(display, self.colorWheel, wheel2)
        pygame.draw.polygon(display, self.colorGun, self.gunCoord)
        if self.level == 4:
            pygame.draw.polygon(display, self.colorGun, self.gunCoord2)
        pygame.draw.polygon(display, self.colorHead, head)
        if self.level == 2:
            pygame.draw.ellipse(display, self.colorBase, (self.barrelX - self.r/4, self.barrelY - self.r/4, self.r/2, self.r/2))
        if self.level >= 3:
            coord = getCoordPoly(self.barrelX, self.barrelY, self.r/3, 3, rotate)
            pygame.draw.polygon(display, self.colorBase, coord)
            
        #pygame.draw.ellipse(display, (123, 125, 125), (self.x - self.range/2, self.y - self.range/2, self.range, self.range), 1)
                
    def move(self, defenceStruct):
        if len(defenceStruct):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in defenceStruct:
                dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                if lowestDist > dist:
                    self.nearestPos = [struct.x, struct.y]
                    lowestDist = dist
        else:
            self.nearestPos = pygame.mouse.get_pos()
        
        #self.nearestPos = pygame.mouse.get_pos()
        angle = atan2(self.nearestPos[1] - self.y, self.nearestPos[0] - self.x)
        self.x += self.speed*cos(angle)
        self.y += self.speed*sin(angle)
        self.barrelX += self.speed*cos(angle)
        self.barrelY += self.speed*sin(angle)
        
        dist = abs(self.nearestPos[1] - self.y) + abs(self.nearestPos[0] - self.x)
        if dist < self.range/2:
            self.speed = 0
        else:
            self.speed = self.speedMemory


class Helicopter:
    def __init__(self, x, y, r, speed, range, level, shotSpeed=5, radius=2):
        self.x = x
        self.y = y
        self.barrelX = x
        self.barrelY = y

        self.range = range
        self.shotSpeed = shotSpeed
        self.radius = radius
        
        self.r = r
        self.speed = speed
        self.speedMemory = speed

        self.level = level

        if self.level == 1:
            self.colorFront = (26, 82, 118)
            self.colorBody = (26, 82, 118)
            self.colorTail = (26, 82, 118)
            self.colorTailHead = (26, 82, 118)
            self.colorFan = (23, 32, 42)
            self.colorGun = (23, 32, 42)
            self.hitPoint = 700
            self.damage = 30
        elif self.level == 2:
            self.colorFront = (11, 83, 69)
            self.colorBody = (22, 160, 133)
            self.colorTail = (11, 83, 69)
            self.colorTailHead = (11, 83, 69)
            self.colorFan = (23, 32, 42)
            self.colorGun = (23, 32, 42)
            self.hitPoint = 900
            self.damage = 50
        elif self.level == 3:
            self.colorFront = (28, 40, 51)
            self.colorBody = (21, 67, 96)
            self.colorTail = (28, 40, 51)
            self.colorTailHead = (28, 40, 51)
            self.colorFan = (23, 32, 42)
            self.colorGun = (23, 32, 42)
            self.hitPoint = 1300
            self.damage = 52

        self.angle = 0
        self.rotAngle = 0
        self.fanAngle = 0

        self.type = "AIR"
        
        self.gunCoord = []
        self.gunCoord2 = []
        self.shots = []

        self.nearestPos = None
        self.health = self.hitPoint

        self.delay = 0
        self.font = pygame.font.SysFont("Agency FB", 15)

    def updateHealth(self, defenceStruct):
        error = self.r
        for struct in defenceStruct:
            if not (struct.type == "HEADQUARTERS" or struct.type == "RESOURCE") and (struct.attackType == "AIR" or struct.attackType == "GROUND AND AIR"):
                if (abs(struct.nearestPos[0] - self.x) < error)  and (abs(struct.nearestPos[1] - self.y) < error):
                    for shot in struct.shots:
                        if struct.isHit((shot.x, shot.y)):
                            self.health -= struct.damage
            
    def isHit(self, coord):
        error = self.r
        dist = ((self.nearestPos[0] - coord[0])**2 + (self.nearestPos[1] - coord[1])**2)**0.5
        if dist < error:
            return True
        return False

    def removeHit(self):
        tempList = self.shots[:]
        for shot in self.shots:
            if self.isHit((shot.x, shot.y)):
                tempList.remove(shot)

        self.shots = tempList[:]
                
    def shoot(self):
        self.delay = (self.delay + 1)%100
        
        if self.level == 1:
            if self.speed == 0 and self.rotAngle == -90 and self.delay%7 == 0:
                pos = self.nearestPos
                #pos = pygame.mouse.get_pos()
                dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
                self.angle = atan2(pos[1] - self.y, pos[0] - self.x)
                
                if dist < self.range/2:
                    shot = Shots((self.gunCoord[1][0] + self.gunCoord[2][0])/2, (self.gunCoord[1][1] + self.gunCoord[2][1])/2, self.radius, self.shotSpeed, self.angle, (0, 0, 0), "line")
                    self.shots.append(shot)
        if self.level == 2:
            if self.delay%10 == 0:
                pos = self.nearestPos
                #pos = pygame.mouse.get_pos()
                dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
                self.angle = atan2(pos[1] - self.y, pos[0] - self.x)
                
                if dist < self.range/2:
                    shot = Shots((self.gunCoord[1][0] + self.gunCoord[2][0])/2, (self.gunCoord[1][1] + self.gunCoord[2][1])/2, self.radius, self.shotSpeed, self.angle, (0, 0, 0), "line")
                    self.shots.append(shot)
            
        elif self.level == 3:
            if self.delay%10 == 0:
                pos = self.nearestPos
                #pos = pygame.mouse.get_pos()
                dist = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
                self.angle = atan2(pos[1] - self.y, pos[0] - self.x)
                
                if dist < self.range/2:
                    shot = Shots((self.gunCoord[1][0] + self.gunCoord[2][0])/2, (self.gunCoord[1][1] + self.gunCoord[2][1])/2, self.radius, self.shotSpeed, self.angle, (0, 0, 0), "line")
                    self.shots.append(shot)
                    shot = Shots((self.gunCoord2[1][0] + self.gunCoord2[2][0])/2, (self.gunCoord2[1][1] + self.gunCoord2[2][1])/2, self.radius, self.shotSpeed, self.angle, (0, 0, 0), "line")
                    self.shots.append(shot)
                    
        tempList = self.shots[:]
                
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    
    def rotate(self, coord, angle, anchor=(0, 0), corr=270):
        corr = corr
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord, point=-1):
        if point == -1:
            return [coord[0] + self.x, coord[1] + self.y]
        else:
            return [coord[0] + point[0], coord[1] + point[1]]

    def draw(self):
        #pos = pygame.mouse.get_pos()
        pos = self.nearestPos
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)

        self.fanAngle = (self.fanAngle + 46)%360

        len = (self.r*2)/(3**0.5)
        
        centre = (self.x, self.y)
        top = (self.x + len*cos(radians(self.fanAngle)), self.y + len*sin(radians(self.fanAngle)))
        left = (self.x + len*cos(radians(self.fanAngle - 120)), self.y + len*sin(radians(self.fanAngle - 120)))
        right = (self.x + len*cos(radians(self.fanAngle + 120)), self.y + len*sin(radians(self.fanAngle + 120)))

        w = self.r/2
        h = self.r/2

        if self.level >= 2:
            w = self.r/4
            h = self.r/2
        
        points = [(0, 0), (0, h), (w, h), (w, 0)]
        base = []

        if self.speed == 0 and self.rotAngle > -90 and self.level == 1:
            self.rotAngle -= 3
        
        for point in points:
            base.append(self.translate(self.rotate(point, rotate + radians(self.rotAngle), (w/2, h/2))))

        front = getCoordPoly((base[1][0] + base[2][0])/2, (base[1][1] + base[2][1])/2, w/2, 8, rotate + radians(self.rotAngle))
        if self.level >= 2:
            back = getCoordPoly((base[0][0] + base[3][0])/2, (base[0][1] + base[3][1])/2, w, 8, rotate + radians(self.rotAngle))
        else:
            back = getCoordPoly((base[0][0] + base[3][0])/2, (base[0][1] + base[3][1])/2, w/2, 8, rotate + radians(self.rotAngle))
        tail = []
        
        if self.level >= 2:                
            w = self.r/3
            h = self.r/2

            points = [(0, 0), (0, h), (w, h), (w, 0)]
            base2 = []

            for point in points:
                base2.append(self.translate(self.rotate(point, rotate + radians(self.rotAngle), (w/2, h*2/3))))

            flap1 = []
            flap2 = []
            w = self.r/3
            h = self.r/4

            points = [(0, 0), (0, h), (w, h), (w, 0)]

            for point in points:
                flap1.append(self.translate(self.rotate(point, rotate + radians(self.rotAngle), (w/2 + w, h))))
                flap2.append(self.translate(self.rotate(point, rotate + radians(self.rotAngle), (w/2 - w, h))))

        w = self.r/8
        h = self.r*1.2
        points = [(0, 0), (0, h), (w, h), (w, 0)]
        
        for point in points:
            tail.append(self.translate(self.rotate(point, rotate + radians(self.rotAngle), (w/2, h))))

        if self.level == 1:
            self.gunCoord = []
            w = self.r/15
            h = self.r/2.5
            points = [(0, 0), (0, h), (w, h), (w, 0)]

            for point in points:
                self.gunCoord.append(self.translate(self.rotate(point, rotate + radians(90) + radians(self.rotAngle), (w/2, 0))))
        elif self.level == 2:
            self.gunCoord = []
            w = self.r/15
            h = self.r/2.5
            points = [(0, 0), (0, h), (w, h), (w, 0)]

            for point in points:
                self.gunCoord.append(self.translate(self.rotate(point, rotate + radians(180) + radians(self.rotAngle), (w/2, h*3/2))))
        elif self.level == 3:
            self.gunCoord = []
            self.gunCoord2 = []
            w = self.r/15
            h = self.r/2.5
            points = [(0, 0), (0, h), (w, h), (w, 0)]

            for point in points:
                self.gunCoord.append(self.translate(self.rotate(point, rotate + radians(180) + radians(self.rotAngle), (w/2 + 5*w, h/2))))
                self.gunCoord2.append(self.translate(self.rotate(point, rotate + radians(180) + radians(self.rotAngle), (w/2 - 5*w, h/2))))
            
        tailHead = []
        w = self.r/10
        h = self.r/3
        points = [(0, 0), (0, h), (w, h), (w, 0)]

        for point in points:
            tailHead.append(self.translate(self.rotate(point, rotate + radians(90) + radians(self.rotAngle), (self.r + w, h/2))))


        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r*2, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r*2 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))
                
        pygame.draw.polygon(display, self.colorFront, front)
        pygame.draw.polygon(display, self.colorGun, self.gunCoord)
        pygame.draw.polygon(display, self.colorBody, back)
        pygame.draw.polygon(display, self.colorBody, base)
        if self.level >= 2:
            pygame.draw.polygon(display, self.colorBody, base2)
            pygame.draw.polygon(display, self.colorFront, flap1)
            pygame.draw.polygon(display, self.colorFront, flap2)
        if self.level == 3:
            pygame.draw.polygon(display, self.colorGun, self.gunCoord2)
        pygame.draw.polygon(display, self.colorTail, tail)
        pygame.draw.polygon(display, self.colorTailHead, tailHead)
        
        pygame.draw.line(display, self.colorFan, top, centre, 5)
        pygame.draw.line(display, self.colorFan, left, centre, 5)
        pygame.draw.line(display, self.colorFan, right, centre, 5)

    def move(self, defenceStruct):
        if len(defenceStruct):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in defenceStruct:
                if struct.type == "HEADQUARTERS" or struct.type == "RESOURCE":
                    dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                else:
                    dist = (self.x - struct.xOld)**2 + (self.y - struct.yOld)**2
                if lowestDist > dist:
                    if struct.type == "HEADQUARTERS" or struct.type == "RESOURCE":
                        self.nearestPos = [struct.x, struct.y]
                    else:
                        self.nearestPos = [struct.xOld, struct.yOld]
                    lowestDist = dist
        else:
            self.nearestPos = pygame.mouse.get_pos()
        
        #self.nearestPos = pygame.mouse.get_pos()
        angle = atan2(self.nearestPos[1] - self.y, self.nearestPos[0] - self.x)
        self.x += self.speed*cos(angle)
        self.y += self.speed*sin(angle)

        dist = abs(self.nearestPos[1] - self.y) + abs(self.nearestPos[0] - self.x)
        if dist < self.range/2:
            self.speed = 0
        else:
            self.speed = self.speedMemory
            self.rotAngle = 0
    
