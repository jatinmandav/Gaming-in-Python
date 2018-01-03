"""
~~~~~~~
Maps.py
~~~~~~~

By - JATIN KUMAR MANDAV

This library contains the MAPS class which  contains major;y two function, openMap() and createMap()

The user can open the predefined or their saved custom maps using openMap() or
Can save their oen designed custom maps using createMap()

This is completely coded using PYGAME library of PYTHON 2.7

Lines - 809

"""

# Imports
import pygame
import sys
from math import *
from GUI import *
from Structures import *
from Troops import *

width = 0
height = 0
display = None
margin = 0

clock = pygame.time.Clock()

groundW = 0
groundH = 0
validW = 0
validH = 0

margin2 = 0

white = (255, 255, 255)
black = (0, 0, 0)
yellow = (241, 196, 15)
red = (203, 67, 53)
green = (30, 132, 73)
blue = (36, 113, 163)
gray = (113, 125, 126)
darkGray = (23, 32, 42)

activeButton = 1
presentLevel = 1

victory = False
stars = 0

canInfo = {"w":10, "h":33, "size":33, "range":200, "baseR":25, "shotR":7,
            "shotSpeed":5}
mortarInfo = {"w": 25, "h":25, "r":50, "range":300, "shotR":7, "shotSpeed":7}
towerInfo = {"w": 5, "h":30, "size":20, "range":300, "baseR":25, "shotR":7,
            "shotSpeed":10}
hqInfo = {"r":50}

def initMaps(screen, size, border=0, border2=0):
    global width, height, display, margin, groundW, groundH, validW, validH, margin2
    display = screen
    width = size[0]
    height = size[1]
    margin = border

    groundW = width - 150 - 2*margin
    groundH = height - 2*margin

    margin2 = border2
    
    validW = width - 2*margin2 - 150
    validH = height - 2*margin2

    initGUI(display, (width, height))
    initStruct(display, (groundW, groundH), margin)
    initTroops(display, (groundW, groundH), margin)
    
    
def active(num):
    global activeButton
    activeButton = num

def levelActive(num):
    global presentLevel
    presentLevel = num


# Saves the custom maps created by user or "guest"
def saveMap(defenceStruct, user="guest"):
    global structure, noCannon, noMortar, noTower, noHquart, noResource

    if len(defenceStruct) > 0:
        noCannon = 0
        noMortar = 0
        noTower = 0
        noHquart = 0
        noResource = 0

        cannons = []
        mortars = []
        towers = []
        headquarter = []
        resources = []

        for struct in defenceStruct:
            if struct.type == "CANNON":
                cannons.append(struct)
            elif struct.type == "MORTAR":
                mortars.append(struct)
            elif struct.type == "TOWER":
                towers.append(struct)
            elif struct.type == "HEADQUARTERS":
                headquarter.append(struct)
            elif struct.type == "RESOURCE":
                resources.append(struct)

        if user == "admin":
            fmap = open("Data/maps", "a")
        else:
            fmap = open("Data/customMaps", "a")
        for struct in cannons:
            fmap.write(str(struct.x) + "," + str(struct.y) + "," + str(struct.level) + "/")
        fmap.write("|")
        for struct in mortars:
            fmap.write(str(struct.x) + "," + str(struct.y) + "," + str(struct.level) + "/")
        fmap.write("|")
        for struct in towers:
            fmap.write(str(struct.x) + "," + str(struct.y) + "," + str(struct.level) + "/")
        fmap.write("|")
        for struct in headquarter:
            fmap.write(str(struct.x) + "," + str(struct.y) + "," + str(struct.level - 1) + "/")
        fmap.write("|")
        for struct in resources:
            fmap.write(str(struct.x) + "," + str(struct.y) + "/")
        fmap.write("\n")

        fmap.close()
        structure = []

    
# Button to show the damage progress and stars earned
damageButton = Button(10, 10, 300, 130, (51, 51, 51), (51, 51, 51))

star1 = pygame.image.load("Images/1-stars.png")
size = star1.get_size()
star01 = pygame.transform.scale(star1, (size[0]/5, size[1]/5))

star2 = pygame.image.load("Images/2-stars.png")
size = star2.get_size()
star02 = pygame.transform.scale(star2, (size[0]/5, size[1]/5))

star3 = pygame.image.load("Images/3-stars.png")
size = star3.get_size()
star03 = pygame.transform.scale(star3, (size[0]/5, size[1]/5))

def damageDone(fraction, structs):
    global victory, stars
    hqThere = False
    for struct in structs:
        if struct.type == "HEADQUARTERS":
            hqThere = True
            break
        
    percent = int(float(fraction)*100)
    if percent == 100:
        damageButton.addImage(star03, (damageButton.w/2, damageButton.h/2 - 30))
        victory = True
        stars = 3
    elif not hqThere and percent >= 50:
        damageButton.addImage(star02, (damageButton.w/2, damageButton.h/2 - 30))
        victory = True
        stars = 2
    elif (percent >= 50) or (not hqThere and percent < 50):
        damageButton.addImage(star01, (damageButton.w/2, damageButton.h/2 - 30))
        victory = True
        stars = 1
    elif percent < 50 and hqThere:
        damageButton.image = None
        victory = False
        stars = 0
    damageButton.draw()
    pygame.draw.rect(display, (208, 211, 212), (damageButton.x + 50, damageButton.y + damageButton.h - 50, 200, 30))
    w = 2*percent
    pygame.draw.rect(display, (142, 68, 173), (damageButton.x + 50 + 1, damageButton.y + damageButton.h - 50 + 1, w - 2, 30 - 2))

def drawBorder():
    pygame.draw.rect(display, black, (margin, margin, groundW, groundH), 2)

def close():
    pygame.quit()
    sys.exit()

# Pause the Game
def pause():
    font = pygame.font.SysFont("Showcard Gothic", 70)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_m:
                    global loop
                    loop = False
                    return
                
        pauseText = font.render("PAUSED", True, (255, 255, 200))
        resume = font.render("\'ESCAPE\' to RESUME", True, (140, 200, 50))
        main = font.render("\'M\' to MAIN MENU", True, (200, 200, 255))
        quit = font.render("\'Q\' to QUIT", True, (200, 255, 200))

        display.blit(pauseText, (200, height/2 - 150))
        display.blit(resume, (200, height/2 - 50))
        display.blit(main, (200, height/2 + 50))
        display.blit(quit, (200, height/2 + 150))

        pygame.display.update()
        clock.tick(60)

# Maps class
class Maps:
    def __init__(self):
        fmap = open("Data/maps", "r")
        data = fmap.read().split("\n")
        fmap .close()
        data.pop(-1)

        for i in range(len(data)):
            data[i] = data[i].split("|")
            for j in range(len(data[i])):
                data[i][j] = data[i][j].split("/")
                if len(data[i][j]) > 1:
                    data[i][j].pop(-1)
                if not (data[i][j] == ['']):
                    for k in range(len(data[i][j])):
                        data[i][j][k] = [int(float(x)) for x in data[i][j][k].split(",")]
        
        self.maps = data[:]

        fp = open("Data/mapReached", "rb")
        self.mapNum = int(float(fp.read()))
        fp.close()

        fmap = open("Data/customMaps", "r")
        data = fmap.read().split("\n")
        fmap.close()
        data.pop(-1)
        
        for i in range(len(data)):
            data[i] = data[i].split("|")
            for j in range(len(data[i])):
                data[i][j] = data[i][j].split("/")
                if len(data[i][j]) > 1:
                    data[i][j].pop(-1)
                if not (data[i][j] == ['']):
                    for k in range(len(data[i][j])):
                        data[i][j][k] = [int(float(x)) for x in data[i][j][k].split(",")]
        
        self.customMaps = data[:]

        self.mode = "adventure"
        self.font = pygame.font.SysFont("Agency FB", 100)
    
    def createMap(self):
        global presentLevel, loop
        global structure, noCannon, noMortar, noTower , noHquart, noResource
        loop = True
    
        maxCannon = 4
        maxMortar = 2
        maxTower = 4
        maxHquart = 1
        maxResource = 10

        noCannon = 0
        noMortar = 0
        noTower = 0
        noHquart = 0
        noResource = 0

        canMaxLevel = 4
        morMaxLevel = 3
        towMaxLevel = 4
        hqMaxLevel = 5

        structure = []

        level = []
        for i in range(5):
            h = 40
            w = 40
            x = 100*(i + 1) + w*i
            y = margin + 20
            newButton = Button(x, y, w, h, blue, (93, 173, 226), levelActive)
            newButton.arg = i + 1
            newButton.addText(str(i+1), (0, 0), 20)
            level.append(newButton)
        
        inventory = []
        
        for i in range(5):
            h = 100
            x = width - 140
            y = 10*(i + 1) + h*i
            newButton = Button(x, y, 130, h, blue, (93, 173, 226), active)
            inventory.append(newButton)

        save = Button(width - 140, height - 70, 130, 50, blue, (93, 173, 226), saveMap)
        save.addText("SAVE MAP", (0, 0), 20)

        inventory[0].addText("CANNONS" + ": " + str(maxCannon), (0, 0), 20)
        inventory[1].addText("MORTARS" + ": " + str(maxMortar), (0, 0), 20)
        inventory[2].addText("TOWERS" + ": " + str(maxTower), (0, 0), 20)
        inventory[3].addText("HEADQUARTERS" + ": " + str(maxHquart), (0, 0), 20)
        inventory[4].addText("RESOURCE" + ": " + str(maxResource), (0, 0), 20)

        inventory[0].arg = 1
        inventory[1].arg = 2
        inventory[2].arg = 3
        inventory[3].arg = 4
        inventory[4].arg = 5

        while loop:
            inventory[0].updateText("CANNONS" + ": " + str(maxCannon - noCannon), (0, 0))
            inventory[1].updateText("MORTARS" + ": " + str(maxMortar - noMortar), (0, 0))
            inventory[2].updateText("TOWERS" + ": " + str(maxTower - noTower), (0, 0))
            inventory[3].updateText("H.Q." + ": " + str(maxHquart - noHquart), (0, 0))
            inventory[4].updateText("RESOURCE" + ": " + str(maxResource - noResource), (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or pygame.key == pygame.K_p:
                        pause()
                    if event.key == pygame.K_z and len(structure):
                        type = structure[len(structure) - 1].type
                        if type == "CANNON":
                            structure.pop(-1)
                            noCannon -= 1
                        elif type == "MORTAR":
                            structure.pop(-1)
                            noMortar -= 1
                        elif type == "TOWER":
                            structure.pop(-1)
                            noTower -= 1
                        elif type == "H.Q. ":
                            structure.pop(-1)
                            noHquart  -= 1
                        elif type == "RESOURCE":
                            structure.pop(-1)
                            noResource  -= 1
                            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inventory[0].select()
                    inventory[1].select()
                    inventory[2].select()
                    inventory[3].select()
                    inventory[4].select()

                    level[0].select()
                    level[1].select()
                    level[2].select()
                    level[3].select()
                    level[4].select()
                    
                    save.arg = structure
                    save.select()
                    
                    pos = pygame.mouse.get_pos()
                    if (margin < pos[0] < groundW + margin) and (margin < pos[1] < groundH + margin):
                        if (margin2 < pos[0] < validW + margin2) and (margin2 < pos[1] < validH + margin2):
                            if activeButton == 1 and noCannon < maxCannon:
                                if presentLevel > canMaxLevel:
                                    presentLevel = canMaxLevel
                                newCannon = Cannon(pos[0], pos[1], canInfo["w"], canInfo["h"], canInfo["size"], canInfo["range"], canInfo["baseR"],
                                                   presentLevel, canInfo["shotR"], canInfo["shotSpeed"])
                                structure.append(newCannon)
                                noCannon += 1
                            if activeButton == 2 and noMortar < maxMortar:
                                if presentLevel > morMaxLevel:
                                    presentLevel = morMaxLevel
                                newMortar = Mortar(pos[0], pos[1], mortarInfo["w"], mortarInfo["h"], mortarInfo["r"], mortarInfo["range"],
                                                   presentLevel, mortarInfo["shotR"],
                                                   mortarInfo["shotSpeed"])
                                structure.append(newMortar)
                                noMortar += 1
                            if activeButton == 3 and noTower < maxTower:
                                if presentLevel > towMaxLevel:
                                    presentLevel = towMaxLevel
                                newTower = Tower(pos[0], pos[1], towerInfo["w"], towerInfo["h"], towerInfo["size"], towerInfo["range"],
                                                 towerInfo["baseR"], presentLevel, towerInfo["shotR"], towerInfo["shotSpeed"])
                                structure.append(newTower)
                                noTower += 1
                            if activeButton == 4 and noHquart < maxHquart:
                                if presentLevel > hqMaxLevel:
                                    presentLevel = hqMaxLevel
                                newHQ = HeadQuarters(pos[0], pos[1], hqInfo["r"], presentLevel)
                                structure.append(newHQ)
                                noHquart += 1
                            if activeButton == 5 and noResource < maxResource:
                                newResource = Resource(pos[0], pos[1])
                                structure.append(newResource)
                                noResource += 1
                                
            display.fill((154,102,64))
            pygame.draw.rect(display, (195,151,98), (margin, margin, groundW, groundH))
            pygame.draw.rect(display, (154,102,64), (margin2, margin2, validW, validH))
            
            drawBorder()
            pygame.draw.rect(display, gray, (width - 150, 0, 150, height))
            
            for struct in structure:
                if struct.type == "HEADQUARTERS" or struct.type == "RESOURCE":
                    struct.draw()
                else:
                    struct.draw([])
                    struct.shoot()

            for item in inventory:
                item.draw(activeButton)

            if activeButton == 1:
                for i in range(canMaxLevel):
                    level[i].draw(presentLevel)
            elif activeButton == 2:
                for i in range(morMaxLevel):
                    level[i].draw(presentLevel)
            elif activeButton == 3:
                for i in range(towMaxLevel):
                    level[i].draw(presentLevel)
            elif activeButton == 4:
                for i in range(hqMaxLevel):
                    level[i].draw(presentLevel)
                
            save.draw()
                
            pygame.display.update()
            clock.tick(60)

    def showResult(self):
        def quitGame(event=0):
            global loop
            loop = False
        if victory:
            if self.mode == "adventure":
                fp = open("Data/mapReached", "wb")
                fp.write(str(self.mapNum + 1))
                fp.close()
                fp = open("Data/mapReached", "rb")
                print(fp.read())
                fp.close()
            text = self.font.render("VICTORY", True, (255, 255, 255))
        else:
            text = self.font.render("LOSS", True, (255, 255, 255))

        last = False
        if self.mode == "adventure":
            if victory and self.mapNum == len(self.maps) - 1:
                endReached = self.font.render("All Bases Conquered!", True, (200, 200, 200))
                pos2 = endReached.get_rect()
                pos2.center = [width/2, 200]
                last = True
                
        if stars == 1:
            pos = star1.get_rect()
            pos.center = [width/2, height/2]
            display.blit(star1, pos)
        elif stars == 2:
            pos = star2.get_rect()
            pos.center = [width/2, height/2]
            display.blit(star2, pos) 
        elif stars == 3:
            pos = star3.get_rect()
            pos.center = [width/2, height/2]
            display.blit(star3, pos)
        
        pos = text.get_rect()
        pos.center = [width/2, height/2]

        if victory:
            next = Button(width/2 - 100 - 150, height/2 + 200, 200, 100, blue, blue, self.openMap)
            if last:
                next.addText("START AGAIN", (0, 0), 30)
            else:
                next.addText("NEXT MAP", (0, 0), 30)
            next.arg = [1, self.mode]
        else:
            next = Button(width/2 - 100 - 150, height/2 + 200, 200, 100, blue, blue, self.openMap)
            next.addText("ATTACK AGAIN", (0, 0), 30)
            next.arg = [0, self.mode]

        quit = Button(width/2 - 100 + 150, height/2 + 200, 200, 100, blue, blue, quitGame)
        quit.addText("QUIT", (0, 0), 30)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    next.select()
                    quit.select()

            display.blit(text, pos)

            if last:
                display.blit(endReached, pos2)

            next.draw()
            quit.draw()

            if not loop:
                return
            
            clock.tick(60)
            pygame.display.update()
            
    def openMap(self, arg):
        global loop
        self.mode = arg[1]
        
        loop = True
        global presentLevel

        defenceStruct = []
        
        if self.mode == "adventure":
            self.mapNum = (self.mapNum + arg[0])%len(self.maps)
        else:
            self.mapNum = (self.mapNum + arg[0])%len(self.customMaps)
            
        if self.mode == "adventure":
            map = self.maps[self.mapNum]
        else:
            map = self.customMaps[self.mapNum]

        cannonCoord = map[0]
        mortarCoord = map[1]
        towerCoord = map[2]
        hqCoord = map[3]
        resourceCoord = map[4]

        if not (cannonCoord == [""]):
            for pos in cannonCoord:
                newCannon = Cannon(pos[0], pos[1], canInfo["w"], canInfo["h"], canInfo["size"],
                                    canInfo["range"], canInfo["baseR"], pos[2],
                                    canInfo["shotR"], canInfo["shotSpeed"])
                defenceStruct.append(newCannon)
        if not (mortarCoord == [""]):                
            for pos in mortarCoord:
                newMortar = Mortar(pos[0], pos[1], mortarInfo["w"], mortarInfo["h"], mortarInfo["r"],
                                    mortarInfo["range"], pos[2], mortarInfo["shotR"],
                                    mortarInfo["shotSpeed"])
                defenceStruct.append(newMortar)

        if not (towerCoord == [""]):
            for pos in towerCoord:
                newTower = Tower(pos[0], pos[1], towerInfo["w"], towerInfo["h"], towerInfo["size"],
                                    towerInfo["range"], towerInfo["baseR"], pos[2],
                                    towerInfo["shotR"], towerInfo["shotSpeed"])
                defenceStruct.append(newTower)              

        if not (hqCoord == [""]):
            for pos in hqCoord:
                newHQ = HeadQuarters(pos[0], pos[1], hqInfo["r"], pos[2])
                defenceStruct.append(newHQ)
                
        if not (resourceCoord == [""]):
            for pos in resourceCoord:
                newResource = Resource(pos[0], pos[1])
                defenceStruct.append(newResource)

        if self.mode == "custom":
            level = []
            for i in range(5):
                h = 40
                w = 40
                x = width - 75 - 20
                y = height/2 + (h + 10)*i 
                newButton = Button(x, y, w, h, blue, (93, 173, 226), levelActive)
                newButton.arg = i + 1
                newButton.addText(str(i+1), (0, 0), 20)
                level.append(newButton)

        troops = []

        inventory = []
        for i in range(3):
            h = 100
            x = width - 140
            y = 10*(i + 1) + h*i
            newButton = Button(x, y, 130, h, blue, (93, 173, 226), active)
            inventory.append(newButton)

        if self.mode == "custom":
            maxShooter = 20
            maxTank = 5
            maxHeli = 3
            shooterMaxLevel = 5
            tankMaxLevel = 4
            heliMaxLevel = 3
        else:
            if self.mapNum < 4:        
                maxShooter = 12
                maxTank = 0
                maxHeli = 0
                shooterMaxLevel = 1
                tankMaxLevel = 0
                heliMaxLevel = 0
            elif self.mapNum < 8:        
                maxShooter = 15
                maxTank = 1
                maxHeli = 0
                shooterMaxLevel = 2
                tankMaxLevel = 1
                heliMaxLevel = 0
            elif self.mapNum < 12:        
                maxShooter = 15
                maxTank = 2
                maxHeli = 1
                shooterMaxLevel = 3
                tankMaxLevel = 2
                heliMaxLevel = 1
            elif self.mapNum < 16:        
                maxShooter = 18
                maxTank = 3
                maxHeli = 2
                shooterMaxLevel = 4
                tankMaxLevel = 3
                heliMaxLevel = 2
            else:       
                maxShooter = 20
                maxTank = 5
                maxHeli = 3
                shooterMaxLevel = 5
                tankMaxLevel = 4
                heliMaxLevel = 3

        if self.mode == "custom":
            next = Button(width - 130, height - 100, 100, 40, blue, blue, self.openMap)
            next.addText("NEXT MAP", (0, 0), 20)
            next.arg = [1, self.mode]

        noShooter = 0
        noTank = 0
        noHeli = 0
        
        inventory[0].addText("SHOOTER" + ": " + str(maxShooter), (0, 0), 20)
        inventory[1].addText("TANK" + ": " + str(maxTank), (0, 0), 20)
        inventory[2].addText("HELICOPTER" + ": " + str(maxHeli), (0, 0), 20)
        
        inventory[0].arg = 1
        inventory[1].arg = 2
        inventory[2].arg = 3

        initStruct = len(defenceStruct)

        while loop:
            inventory[0].updateText("SHOOTER" + ": " + str(maxShooter - noShooter), (0, 0))
            inventory[1].updateText("TANK" + ": " + str(maxTank - noTank), (0, 0))
            inventory[2].updateText("HELICOPTER" + ": " + str(maxHeli - noHeli), (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or pygame.key == pygame.K_p:
                        pause()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    inventory[0].select()
                    inventory[1].select()
                    inventory[2].select()

                    if self.mode == "custom":
                        level[0].select()
                        level[1].select()
                        level[2].select()
                        level[3].select()
                        level[4].select()
                        next.select()

                    pos = pygame.mouse.get_pos()
                    if (margin < pos[0] < groundW + margin) and (margin < pos[1] < groundH + margin):
                        if not ((margin2  < pos[0] < margin2 + validW) and (margin2 < pos[1] < margin2 + validH)):
                            if activeButton == 1 and noShooter < maxShooter:
                                if self.mode == "custom":
                                    if presentLevel > shooterMaxLevel:
                                        presentLevel = shooterMaxLevel
                                    newShooter = Shooter(pos[0], pos[1], 5, 1.2, 180, presentLevel, 5, 2)
                                else:
                                    newShooter = Shooter(pos[0], pos[1], 5, 1.2, 180, shooterMaxLevel, 5, 2)
                                troops.insert(0, newShooter)
                                noShooter += 1
                            if activeButton == 2 and noTank < maxTank:
                                if self.mode == "custom":
                                    if presentLevel > tankMaxLevel:
                                        presentLevel = tankMaxLevel
                                    newTank = Tank(pos[0], pos[1], 20, 1, 200, presentLevel, 6, 2)
                                else:
                                    newTank = Tank(pos[0], pos[1], 20, 1, 200, tankMaxLevel, 6, 2)
                                troops.insert(0, newTank)
                                noTank += 1
                            if activeButton == 3 and noHeli < maxHeli:
                                if self.mode == "custom":
                                    if presentLevel > heliMaxLevel:
                                        presentLevel = heliMaxLevel
                                    newHeli = Helicopter(pos[0], pos[1], 30, 0.7, 200, presentLevel, 7, 10)
                                else:
                                    newHeli = Helicopter(pos[0], pos[1], 30, 0.7, 200, heliMaxLevel, 7, 10)
                                troops.append(newHeli)
                                noHeli += 1
                        
            display.fill((154,102,64))
            pygame.draw.rect(display, (195,151,98), (margin, margin, groundW, groundH))
            pygame.draw.rect(display, (154,102,64), (margin2, margin2, validW, validH))
            
            drawBorder()
            pygame.draw.rect(display, gray, (width - 150, 0, 150, height))
            for item in inventory:
                item.draw(activeButton)
            
            for troop in troops:
                troop.move(defenceStruct)
                troop.draw()
                troop.shoot()

                troop.updateHealth(defenceStruct)

            for struct in defenceStruct:
                if not (struct.type == "HEADQUARTERS" or struct.type == "RESOURCE"):
                    struct.removeHit()
            
            for struct in defenceStruct:
                if struct.type == "HEADQUARTERS":
                    struct.draw()
                elif struct.type == "RESOURCE":
                    struct.draw()
                else:
                    struct.draw(troops)
                    struct.shoot()
                    
                struct.updateHealth(troops)

            for troop in troops:
                troop.removeHit()
            
            for struct in defenceStruct:
                if struct.health <= 0:
                    defenceStruct.remove(struct)

            for troop in troops:
                if troop.health <= 0:
                    troops.remove(troop)

            if self.mode == "custom":
                if activeButton == 1:
                    for i in range(shooterMaxLevel):
                        level[i].draw(presentLevel)
                elif activeButton == 2:
                    for i in range(tankMaxLevel):
                        level[i].draw(presentLevel)
                if activeButton == 3 :
                    for i in range(heliMaxLevel):
                        level[i].draw(presentLevel)

            
            if self.mode == "custom" and noShooter == 0 and noTank == 0 and noHeli == 0:
                next.draw()
            
            damageDone(1.0 - float(len(defenceStruct))/initStruct, defenceStruct)
            if (defenceStruct == []) or (noShooter == maxShooter and noTank == maxTank and noHeli == maxHeli and troops == []):
                self.showResult()

            pygame.display.update()
            
            clock.tick(90)



if __name__ == "__main__":
    width = 1260
    height = 720

    screen = pygame.display.set_mode((width, height))

    initMaps(screen, (width, height), 25, 100)
    
    newMap = Maps()
    newMap.openMap([0, "adventure"])
    #newMap.createMap()
    close()
