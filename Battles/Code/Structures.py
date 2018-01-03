"""
~~~~~~~~~~~~~
Structures.py
~~~~~~~~~~~~~

By - JATIN KUMAR MANDAV

This is a library for all structures used in Game
Structures: 1. CANNONS
            2. MORTARS
            3. TOWERS
            4. HEADQUARTERS
            5. RESOURCE BUILDINGS

This is completely coded using PYGAME library of PYTHON 2.7

Lines - 717

"""

# Imports
import pygame
import sys
from math import *
import random

pygame.init()

display = None
width = 0
height = 0
margin = 0

clock = pygame.time.Clock()

def initStruct(screen, size, border=0):
    global display, width, height, margin
    display = screen
    width = size[0]
    height = size[1]
    margin = border

def getCoordPoly(x, y, r, n, rotate=0, anchor=(0, 0)):
    coords = []
    for i in range(n):
        coords.append([x - anchor[0] + r*cos(2*pi*i/n + rotate), y - anchor[1] + r*sin(2*pi*i/n + rotate)])

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

class Cannon:
    def __init__(self, x, y, w, h, size, range, baseR, level, radius, speed, colorBarrel=(0, 0, 0), colorHead=(0, 0, 0), colorBase=(255, 255, 255)):
        self.x = x
        self.y = y

        self.xOld = self.x
        self.yOld = self.y
        self.angle = 0
        
        self.r = size
        self.w = w
        self.h = h
        self.type = "CANNON"
        self.attackType = "GROUND"
        self.baseR = baseR

        self.radius = radius
        self.speed = speed
        
        self.range = range
        self.coord = getCoordPoly(self.x, self.y, self.r, 4)
        self.rectCoord = []

        self.shots = []
        
        self.recoil = 3
        self.rebound = 0.1

        self.level = level

        if self.level == 1:
            self.colorBarrel = (23, 32, 42)
            self.colorHead = (39, 55, 70)
            self.colorBase = (123, 125, 125)
            self.hitPoint = 420
            self.damage = 8
        elif self.level == 2:
            self.colorBarrel = (11, 83, 69)
            self.colorHead = (30, 132, 73)
            self.colorBase = (23, 32, 42)
            self.hitPoint = 640
            self.damage = 33
            self.headCover = (69, 179, 157)
        elif self.level == 3:
            self.colorBarrel = (21, 67, 96)
            self.colorHead = (40, 116, 166)
            self.colorBase = (144, 148, 151)
            self.hitPoint = 830
            self.damage = 32
            self.rectCoord2 = []
        elif self.level == 4:
            self.colorBarrel = (23, 32, 42)
            self.colorHead = (46, 64, 83)
            self.colorBase = (144, 148, 151)
            self.hitPoint = 1200
            self.damage = 54
            self.rectCoord2 = []
            self.headCover = (133, 146, 158)
            
        self.health = self.hitPoint

        self.nearestPos = pygame.mouse.get_pos()

        self.font = pygame.font.SysFont("Agency FB", 20)

    def updateHealth(self, troops):
        error = self.baseR
        for troop in troops:
            if (abs(troop.nearestPos[0] - self.x) < error)  and (abs(troop.nearestPos[1] - self.y) < error):
                for shot in troop.shots:
                    if troop.isHit((shot.x, shot.y)):
                        self.health -= troop.damage

    def isHit(self, coord):
        error = self.baseR
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
                        
    def rotate(self, coord, angle, anchor=(0, 0)):
        corr = 270
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]

    def shoot(self):
        error = 0.05

        if not ((abs(self.x - self.xOld) < error) and (abs(self.y - self.yOld) < error)):
            self.x += self.rebound*cos(self.angle)
            self.y += self.rebound*sin(self.angle)
        else:
            pos = self.nearestPos
            #pos = pygame.mouse.get_pos()
            dist = ((self.xOld - pos[0])**2 + (self.yOld - pos[1])**2)**0.5
            self.angle = atan2(pos[1] - self.yOld, pos[0] - self.xOld)
            
            if dist < self.range/2:
                shot = Shots((self.rectCoord[1][0] + self.rectCoord[2][0])/2, (self.rectCoord[1][1] + self.rectCoord[2][1])/2, self.radius, self.speed, self.angle, (0, 0, 0), "line")
                self.shots.append(shot)
                if self.level >= 3:
                    shot = Shots((self.rectCoord2[1][0] + self.rectCoord2[2][0])/2, (self.rectCoord2[1][1] + self.rectCoord2[2][1])/2, self.radius, self.speed, self.angle, (0, 0, 0), "line")
                    self.shots.append(shot)
                self.x -= self.recoil*cos(self.angle)
                self.y -= self.recoil*sin(self.angle)

        tempList = self.shots[:]
                
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    def draw(self, troops):
        if len(troops):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in troops:
                if struct.type == "GROUND":
                    dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                    if lowestDist > dist:
                        self.nearestPos = [struct.x, struct.y]
                        lowestDist = dist
        else:
            self.nearestPos = pygame.mouse.get_pos()

        pos = self.nearestPos
        #pos = pygame.mouse.get_pos()
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)
        
        points = [(0, 0), (0, self.h), (self.w, self.h), (self.w, 0)]

        self.coord = getCoordPoly(self.x, self.y, self.r/2, 6, rotate)

        if self.level <= 3:
            self.rectCoord = []
            
            for point in points:
                self.rectCoord.append(self.translate(self.rotate(point, rotate, (self.w/2, 0))))
        if self.level >= 3:
            w = self.w/2
            h = self.h
            self.rectCoord = []
            self.rectCoord2 = []

            points = [(0, 0), (0, h), (w, h), (w, 0)]

            for point in points:
                self.rectCoord.append(self.translate(self.rotate(point, rotate, (w/2 + w, 0))))
                self.rectCoord2.append(self.translate(self.rotate(point, rotate, (w/2 - w, 0))))


        baseCoord = getCoordPoly(self.xOld, self.yOld, self.baseR, 4, radians(45))

        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.baseR*2, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.baseR*2 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))

        pygame.draw.polygon(display, self.colorBase, baseCoord)
        pygame.draw.polygon(display, self.colorBarrel, self.rectCoord)
        if self.level >= 3:
            pygame.draw.polygon(display, self.colorBarrel, self.rectCoord2)
        pygame.draw.polygon(display, self.colorHead, self.coord)

        if self.level == 2 or self.level == 4:
            pygame.draw.ellipse(display, self.headCover, (self.x - self.baseR/3, self.y - self.baseR/3, self.baseR*2/3, self.baseR*2/3))

        #pygame.draw.ellipse(display, (0, 0, 0), (self.xOld - self.range/2, self.yOld - self.range/2, self.range, self.range), 1)
   
class Tower:
    def __init__(self, x, y, w, h, size, range, baseR, level, radius, speed, colorBarrel=(0, 0, 0), colorHead=(0, 0, 0), colorBase=(255, 0, 0)):
        self.x = x
        self.y = y

        self.xOld = self.x
        self.yOld = self.y
        self.angle = 0
        
        self.r = size
        self.w = w
        self.h = h
        self.type = "TOWER"
        self.baseR = baseR

        self.radius = radius
        self.speed = speed
        
        self.range = range
        self.coord = getCoordPoly(self.x, self.y, self.r, 4)
        self.rectCoord = []

        self.attackType = "GROUND AND AIR"

        self.shots = []
        
        self.recoil = 5
        self.rebound = 0.25

        self.level = level
        
        if self.level == 1:
            self.colorBarrel = (100, 30, 22)
            self.colorHead = (100, 30, 22)
            self.colorBase = (26, 82, 118)
            self.hitPoint = 380
            self.damage = 10
        elif self.level == 2:
            self.colorBarrel = (100, 30, 22)
            self.colorHead = (100, 30, 22)
            self.colorBase = (125, 102, 8)
            self.hitPoint = 580
            self.damage = 30
        elif self.level == 3:
            self.colorBarrel = (183, 149, 11)
            self.colorHead = (185, 119, 14)
            self.colorBase = (11, 83, 69)
            self.colorBase2 = (39, 174, 96)
            self.hitPoint = 810
            self.damage = 60
        elif self.level == 4:
            self.colorBarrel = (23, 32, 42)
            self.colorHead = (52, 73, 94)
            self.colorBase = (21, 67, 96)
            self.colorBase2 = (98, 101, 103)
            self.hitPoint = 1230
            self.damage = 90

        self.health = self.hitPoint
        
        self.nearestPos = pygame.mouse.get_pos()

        self.font = pygame.font.SysFont("Agency FB", 20)

    def updateHealth(self, troops):
        error = self.r
        for troop in troops:
            if (abs(troop.nearestPos[0] - self.x) < error)  and (abs(troop.nearestPos[1] - self.y) < error):
                for shot in troop.shots:
                    if troop.isHit((shot.x, shot.y)):
                        self.health -= troop.damage
    
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
                        
    def rotate(self, coord, angle, anchor=(0, 0)):
        corr = 270
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]

    def shoot(self):
        error = 0.1

        if not ((abs(self.x - self.xOld) < error) and (abs(self.y - self.yOld) < error)):
            self.x += self.rebound*cos(self.angle)
            self.y += self.rebound*sin(self.angle)
        else:
            #pos = pygame.mouse.get_pos()
            pos = self.nearestPos
            dist = ((self.xOld - pos[0])**2 + (self.yOld - pos[1])**2)**0.5
            self.angle = atan2(pos[1] - self.yOld, pos[0] - self.xOld)
            
            if dist < self.range/2:
                shot = Shots((self.rectCoord[1][0] + self.rectCoord[2][0])/2, (self.rectCoord[1][1] + self.rectCoord[2][1])/2, self.radius, self.speed, self.angle, (0, 0, 0), "line")
                self.shots.append(shot)
                self.x -= self.recoil*cos(self.angle)
                self.y -= self.recoil*sin(self.angle)

        tempList = self.shots[:]
                
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    def draw(self, troops):
        if len(troops):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in troops:
                if struct.type == "AIR" or struct.type == "GROUND":
                    dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                    if lowestDist > dist:
                        self.nearestPos = [struct.x, struct.y]
                        lowestDist = dist
                else:
                    self.nearestPos = pygame.mouse.get_pos()
        else:
            self.nearestPos = pygame.mouse.get_pos()
        
        #pos = pygame.mouse.get_pos()
        pos = self.nearestPos
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)

        if self.level == 4:
            w = self.w*2
            h = self.h
            points = [(0, 0), (0, h), (w, h), (w, 0)]
            self.rectCoord = []
            
            for point in points:
                self.rectCoord.append(self.translate(self.rotate(point, rotate, (w/2, 0))))
        else:
            w = self.w
            h = self.h
            points = [(0, 0), (0, h), (w, h), (w, 0)]
            self.rectCoord = []
            
            for point in points:
                self.rectCoord.append(self.translate(self.rotate(point, rotate, (w/2, 0))))

        baseCoord = getCoordPoly(self.xOld, self.yOld, self.baseR, 6)

        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.baseR*2, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.baseR*2 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))

        pygame.draw.polygon(display, self.colorBase, baseCoord)

        if self.level >= 3:
            baseCoord2 = getCoordPoly(self.xOld, self.yOld, self.baseR*3/4, 6)
            pygame.draw.polygon(display, self.colorBase2, baseCoord2)        
        
        pygame.draw.polygon(display, self.colorBarrel, self.rectCoord)
        #pygame.draw.polygon(display, self.colorHead, self.coord)
        pygame.draw.ellipse(display, self.colorHead, (self.x - self.r/2, self.y - self.r/2, self.r, self.r ))

        #pygame.draw.ellipse(display, (0, 0, 0), (self.xOld - self.range/2, self.yOld - self.range/2, self.range, self.range), 1)

class Mortar:
    def __init__(self, x, y, w, h, r, range, level, radius, speed, colorBarrel=(0, 0, 0), colorHead=(0, 0, 0), colorBase=(255, 0, 0)):
        self.x = x
        self.y = y

        self.xOld = self.x
        self.yOld = self.y
        
        self.w = w
        self.h = h
        self.r = r

        self.level = level

        if self.level == 1:
            self.colorBarrel = (95, 106, 106)
            self.colorHead = (46, 64, 83)
            self.colorBase = (146, 43, 33)
            self.range = range
            self.hitPoint = 400
            self.damage = 37
        elif self.level == 2:
            self.colorBarrel = (125, 102, 8)
            self.colorHead = (11, 83, 69)
            self.colorBase = (166, 172, 175)
            self.colorHeadCover = (34, 153, 84)
            self.range = range
            self.hitPoint = 650
            self.damage = 70
        elif self.level == 3:
            self.colorBarrel = (21, 67, 96)
            self.colorHead = (36, 113, 163)
            self.colorBase = (113, 125, 126)
            self.colorBarrelHead = (46, 64, 83)
            self.range = range
            self.hitPoint = 850
            self.damage = 130

        self.radius = radius
        self.speed = speed

        self.type = "MORTAR"
        self.attackType = "GROUND"
        
        self.coord = []
        self.rectCoord = []

        self.shots = []

        self.angle = 0
        self.recoil = 7
        self.rebound = 0.1

        self.health = self.hitPoint
        
        self.font = pygame.font.SysFont("Agency FB", 20)

        self.nearestPos = pygame.mouse.get_pos()

    def updateHealth(self, troops):
        error = 15
        for troop in troops:
            if (abs(troop.nearestPos[0] - self.x) < error)  and (abs(troop.nearestPos[1] - self.y) < error):
                for shot in troop.shots:
                    if troop.isHit((shot.x, shot.y)):
                        self.health -= troop.damage

    def isHit(self, coord):
        error = 50
        dist = ((self.nearestPos[0] - coord[0])**2 + (self.nearestPos[1] - coord[1])**2)**0.5
        if dist < self.r:
            return True
        return False

    def removeHit(self):
        tempList = self.shots[:]
        for shot in self.shots:
            if self.isHit((shot.x, shot.y)):
                tempList.remove(shot)

        self.shots = tempList[:]
                        
    def shoot(self):
        error = 0.05

        if not ((abs(self.x - self.xOld) < error) and (abs(self.y - self.yOld) < error)):
            self.x += self.rebound*cos(self.angle)
            self.y += self.rebound*sin(self.angle)
        else:
            #pos = pygame.mouse.get_pos()
            pos = self.nearestPos
            dist = ((self.xOld - pos[0])**2 + (self.yOld - pos[1])**2)**0.5
            self.angle = atan2(pos[1] - self.yOld, pos[0] - self.xOld)

            if dist < self.range/2:
                self.x -= self.recoil*cos(self.angle)
                self.y -= self.recoil*sin(self.angle)
            
                shot = Shots((self.rectCoord[1][0] + self.rectCoord[2][0])/2, (self.rectCoord[1][1] + self.rectCoord[2][1])/2, self.radius, self.speed, self.angle)
                self.shots.append(shot)

        tempList = self.shots[:]
            
        for shot in self.shots:
            shot.move()
            shot.draw()
            if not ((margin < shot.x < width) and (margin < shot.y < height)):
                tempList.remove(shot)

        self.shots = tempList[:]

    def rotate(self, coord, angle, anchor=(0, 0)):
        corr = 270
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def translate(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]
    
    def draw(self, troops):
        if len(troops):
            nearestPos = 0
            lowestDist = float("inf")
            for struct in troops:
                if  struct.type == "GROUND":
                    dist = (self.x - struct.x)**2 + (self.y - struct.y)**2
                    if lowestDist > dist:
                        self.nearestPos = [struct.x, struct.y]
                        lowestDist = dist
                else:
                    self.neasestPos = pygame.mouse.get_pos()
        else:
            self.nearestPos = pygame.mouse.get_pos()
        
        pos = self.nearestPos
        #pos = pygame.mouse.get_pos()
        rotate = atan2(pos[1] - self.y, pos[0] - self.x)
        
        points = [(0, 0), (0, self.h), (self.w, self.h), (self.w, 0)]
        
        self.coord = getCoordPoly(self.x, self.y, self.w*5/8, 8, rotate)
        
        self.rectCoord = []
        
        for point in points:
            self.rectCoord.append(self.translate(self.rotate(point, rotate, (self.w/2, 0))))

        baseCoord = getCoordPoly(self.xOld, self.yOld, self.r*2/5, 10)

        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))
        
        pygame.draw.polygon(display, self.colorBase, baseCoord)
        pygame.draw.polygon(display, self.colorBarrel, self.rectCoord)
        pygame.draw.polygon(display, self.colorHead, self.coord)
        if self.level == 2:
            coord = getCoordPoly(self.x, self.y, self.w*3/8, 8, rotate)
            pygame.draw.polygon(display, self.colorHeadCover, coord)
        if self.level == 3:
            coord = []
            w = self.w*1.2
            h = self.h/5
            points = [(0, 0), (0, h), (w, h), (w, 0)]
        
            for point in points:
                coord.append(self.translate(self.rotate(point, rotate, (w/2, h/2 - self.h))))
            pygame.draw.polygon(display, self.colorBarrelHead, coord)
        #pygame.draw.ellipse(display, (0, 0, 0), (self.xOld - self.range/2, self.yOld - self.range/2, self.range, self.range), 1)



class HeadQuarters:
    def __init__(self, x, y, r, level, color1=(0, 0, 0), color2=(255, 255, 0)):
        self.x = x
        self.y = y
        self.r = r
        self.type = "HEADQUARTERS"
        self.color1 = (23, 32, 42)
        self.color2 = (113, 125, 126)

        self.level = level + 1
        if self.level == 2:
            self.hitPoint = 570
        elif self.level == 3:
            self.hitPoint = 1500
        elif self.level == 4:
            self.hitPoint = 3000
        elif self.level == 5:
            self.hitPoint = 4500
        elif self.level == 6:
            self.hitPoint = 6000
        
        self.health = self.hitPoint
        self.font = pygame.font.SysFont("Agency FB", 20)
        
    def updateHealth(self, troops):
        error = 15
        for troop in troops:
            if (abs(troop.nearestPos[0] - self.x) < error)  and (abs(troop.nearestPos[1] - self.y) < error):
                for shot in troop.shots:
                    if troop.isHit((shot.x, shot.y)):
                        self.health -= troop.damage
                        
    def draw(self):
        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r*1.5, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r*1.5 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))


        outer = []
        inner = []

        for i in range(self.level):
            coord = getCoordPoly(self.x, self.y, self.r - (2.0/3)*self.r*(i)/(self.level), 5)
            if i == 0:
                outer = coord
            elif i == self.level - 1:
                inner = coord
            if i%2 == 0:
                pygame.draw.polygon(display, self.color1, coord)
            else:
                pygame.draw.polygon(display, self.color2, coord)

        for i in range(5):
            pygame.draw.line(display, self.color2, outer[i], inner[i], 3)

gray = (121, 125, 127)
darkGray = (28, 40, 51)
yellow = (212, 172, 13)
red = (203, 67, 53)
orange = (202, 111, 30)
blue = (36, 113, 163)
green = (17, 122, 101)
violet = (125, 60, 152)

class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.randrange(20, 40)
        self.type = "RESOURCE"
        colors = [gray, darkGray, yellow, red, orange, blue, green, violet]
        self.color1 = random.choice(colors)
        self.color2 = random.choice(colors)

        self.sides = random.randrange(4, 10)

        self.hitPoint = random.randrange(250, 700)
        self.health = self.hitPoint

        self.font = pygame.font.SysFont("Agency FB", 20)
        
    def updateHealth(self, troops):
        error = 15
        for troop in troops:
            if (abs(troop.nearestPos[0] - self.x) < error)  and (abs(troop.nearestPos[1] - self.y) < error):
                for shot in troop.shots:
                    if troop.isHit((shot.x, shot.y)):
                        self.health -= troop.damage
                        
    def draw(self):

        pygame.draw.rect(display, (231, 76, 60), (self.x, self.y - self.r*1.5, 40, 8))
        pygame.draw.rect(display, (0, 255, 0), (self.x + 1, self.y - self.r*1.5 + 1, int(.4*(float(self.health)/self.hitPoint)*100) - 2, 8 - 2))

        outer = []
        inner = []

        level = self.sides
        for i in range(level):
            coord = getCoordPoly(self.x, self.y, self.r - (2.0/3)*self.r*(i)/(self.sides), self.sides)
            if i == 0:
                outer = coord
            elif i == level - 1:
                inner = coord
            if i%2 == 0:
                pygame.draw.polygon(display, self.color1, coord)
            else:
                pygame.draw.polygon(display, self.color2, coord)

        for i in range(level):
            pygame.draw.line(display, self.color2, outer[i], inner[i], 3)
