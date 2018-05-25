'''

    Game: Angry Birds
    File: maps.py

    Contents: Class MAPS, that puts everything in action!

    Requirements: Pygame, sys
    Supporting Modules: physics_engine, interface, objects

    By: Jatin Kumar Mandav

    Blog: https://www.jatinmandav.wordpress.com
    Twitter: @jatinmandav
    YouTube: https://www.youtube.com/mandav

'''
import pygame
import sys

import physics_engine
import objects
import interface

pygame.init()
width = None
height = None
display = None
clock = pygame.time.Clock()

ground = 50

d_velocity = 2.0

def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    height -= ground
    interface.init(display)

def all_rest(pigs, birds, blocks):
    threshold = 0.15
    for pig in pigs:
        if pig.velocity.magnitude >= threshold:
            return False

    for bird in birds:
        if bird.velocity.magnitude >= threshold:
            return False

    for block in blocks:
        if block.velocity.magnitude >= threshold:
            return False

    return True

def close():
    pygame.quit()
    sys.exit()

class Maps:
    def __init__(self):
        self.level = 1
        self.max_level = 15
        self.color = {'background': (51, 51, 51)}
        self.score = 0

    def wait_level(self):
        time = 0
        while time < 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
            time += 1
            clock.tick(1)

        return

    def check_win(self, pigs, birds):
        if pigs == []:
            print("WON!")
            return True
        if (not pigs == []) and birds == []:
            print("LOST!")
            return False

    def pause(self):
        pause_text = interface.Label(700, 200, 400, 200, None, self.color['background'])
        pause_text.add_text("GAME PAUSED", 70, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = interface.Button(350, 500, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.add_text("RESTART", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        resume = interface.Button(750, 500, 300, 100, None, (88, 214, 141), (171, 235, 198))
        resume.add_text("RESUME", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = interface.Button(1150, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        mandav = interface.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        mandav.add_text("MANDAV", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_p:
                        return
                    if event.key == pygame.K_ESCAPE:
                        return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if resume.isActive():
                        return
                    if exit.isActive():
                        exit.action()

            replay.draw()
            resume.draw()
            exit.draw()
            pause_text.draw()
            mandav.draw()

            pygame.display.update()
            clock.tick(60)

    def draw_map(self):
        birds = []
        pigs = []
        blocks = []
        walls = []
        self.score = 0

        if self.level == 1:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 40, 20))
            pigs.append(physics_engine.Pig(1500, height - 40, 20))

            blocks.append(physics_engine.Block(1300, height - 60, 60))

        elif self.level == 2:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1000, height - 40, 20))
            pigs.append(physics_engine.Pig(1400, height - 40, 20))

            blocks.append(physics_engine.Block(1200, height - 60, 60))
            blocks.append(physics_engine.Block(1200, height - 2*35, 60))
            blocks.append(physics_engine.Block(1500, height - 60, 60))

        elif self.level == 3:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1200, height - 60, 30))
            pigs.append(physics_engine.Pig(1300, height - 60, 30))

            blocks.append(physics_engine.Block(1000, height - 100, 100))
            blocks.append(physics_engine.Block(1000, height - 2*60, 100))
            blocks.append(physics_engine.Block(1500, height - 100, 100))
            blocks.append(physics_engine.Block(1500, height - 2*60, 100))

        elif self.level == 4:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1200, 500 - 60, 30))
            pigs.append(physics_engine.Pig(1300, height - 60, 30))

            walls.append(objects.Slab(1000, 450, 500, 20))

            blocks.append(physics_engine.Block(1100, height - 100, 100))

        elif self.level == 5:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1300, 500 - 60, 25))
            pigs.append(physics_engine.Pig(1300, height - 60, 25))

            walls.append(objects.Slab(500, 400, 100, height - 400))
            walls.append(objects.Slab(1000, 450, 500, 30))

            blocks.append(physics_engine.Block(1150, 500 - 100, 100))
            blocks.append(physics_engine.Block(1100, height - 100, 100))

        elif self.level == 6:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1300, 500 - 60, 25))
            pigs.append(physics_engine.Pig(1300, height - 60, 25))

            walls.append(objects.Slab(1000, 0, 30, 450))
            walls.append(objects.Slab(1000, 450, 500, 30))

            blocks.append(physics_engine.Block(1150, 500 - 100, 100))
            blocks.append(physics_engine.Block(1100, height - 100, 100))

        elif self.level == 7:
            for i in range(4):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, 500 - 60, 25))
            pigs.append(physics_engine.Pig(1300, 500 - 60, 25))
            pigs.append(physics_engine.Pig(1200, height - 60, 25))

            walls.append(objects.Slab(1200, 250, 30, 200))
            walls.append(objects.Slab(1000, 450, 500, 30))

        elif self.level == 8:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1200, height - 60, 25))

            walls.append(objects.Slab(700, 250, 30, height - 250))

        elif self.level == 9:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))


            blocks.append(physics_engine.Block(1250, height - 100, 100))
            blocks.append(physics_engine.Block(1250, height - 2*60, 100))

            walls.append(objects.Slab(700, 400, 30, height - 400))

        elif self.level == 10:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))

            blocks.append(physics_engine.Block(1250, height - 100, 100))
            blocks.append(physics_engine.Block(1250, height - 2*60, 100))
            blocks.append(physics_engine.Block(900, height - 100, 100))

            walls.append(objects.Slab(900, 400, 500, 30))

        elif self.level == 11:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))

            blocks.append(physics_engine.Block(1250, height - 100, 100))
            blocks.append(physics_engine.Block(1250, height - 2*60, 100))

            walls.append(objects.Slab(900, 400, 500, 30))
            walls.append(objects.Slab(900, 400, 30, height - 400))

        elif self.level == 12:
            for i in range(3):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))

            walls.append(objects.Slab(900, 400, 500, 30))
            walls.append(objects.Slab(1200, 500, 30, height - 500))

        elif self.level == 13:
            for i in range(4):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1200, 400 - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))

            blocks.append(physics_engine.Block(900, height - 100, 100))
            blocks.append(physics_engine.Block(900, height - 2*60, 100))

            walls.append(objects.Slab(900, 400, 500, 40))
            walls.append(objects.Slab(1200, 500, 30, height - 500))

        elif self.level == 14:
            for i in range(4):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(1100, height - 60, 25))
            pigs.append(physics_engine.Pig(1100, 400 - 60, 25))
            pigs.append(physics_engine.Pig(1450, height - 60, 25))

            blocks.append(physics_engine.Block(900, height - 100, 100))

            blocks.append(physics_engine.Block(1300, 400 - 100, 100))

            walls.append(objects.Slab(900, 400, 500, 40))
            walls.append(objects.Slab(900, 0, 30, 400))

        elif self.level == 15:
            for i in range(5):
                new_bird = physics_engine.Bird(40*i + 5*i, height - 40, 20, None, "BIRD")
                birds.append(new_bird)

            pigs.append(physics_engine.Pig(900, height - 60, 25))
            pigs.append(physics_engine.Pig(width - 400, 400 - 60, 25))
            pigs.append(physics_engine.Pig(1700, height - 60, 25))


            walls.append(objects.Slab(800, 400, 30, height - 400))
            walls.append(objects.Slab(1000, 500, 30, height - 500))

            walls.append(objects.Slab(width - 500, 400, 500, 40))
            walls.append(objects.Slab(width - 500, 150, 60, 400 - 150))


        self.start_level(birds, pigs, blocks, walls)

    def replay_level(self):
        self.level -= 1
        self.draw_map()

    def start_again(self):
        self.level = 1
        self.draw_map()

    def level_cleared(self):
        self.level += 1

        level_cleared_text = interface.Label(700, 100, 400, 200, None, self.color['background'])
        if self.level <= self.max_level:
            level_cleared_text.add_text("LEVEL " + str(self.level - 1) + " CLEARED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))
        else:
            level_cleared_text.add_text("ALL LEVEL CLEARED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        score_text = interface.Label(750, 300, 300, 100, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = interface.Button(350, 500, 300, 100, self.replay_level, (244, 208, 63), (247, 220, 111))
        replay.add_text("PLAY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        if self.level <= self.max_level:
            next = interface.Button(750, 500, 300, 100, self.draw_map, (88, 214, 141), (171, 235, 198))
            next.add_text("CONTINUE", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])
        else:
            next = interface.Button(750, 500, 300, 100, self.start_again, (88, 214, 141), (171, 235, 198))
            next.add_text("START AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = interface.Button(1150, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        mandav = interface.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        mandav.add_text("MANDAV", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if next.isActive():
                        next.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            next.draw()
            exit.draw()
            level_cleared_text.draw()
            score_text.draw()
            mandav.draw()

            pygame.display.update()
            clock.tick(60)

    def level_failed(self):
        level_failed_text = interface.Label(700, 100, 400, 200, None, self.color['background'])
        level_failed_text.add_text("LEVEL FAILED!", 80, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        score_text = interface.Label(750, 300, 300, 100, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 55, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        replay = interface.Button(500, 500, 300, 100, self.draw_map, (244, 208, 63), (247, 220, 111))
        replay.add_text("TRY AGAIN", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        exit = interface.Button(1000, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", self.color['background'])

        mandav = interface.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        mandav.add_text("MANDAV", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.isActive():
                        replay.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            exit.draw()
            level_failed_text.draw()
            score_text.draw()
            mandav.draw()

            pygame.display.update()
            clock.tick(60)

    def start_level(self, birds, pigs, blocks, walls):
        loop = True

        slingshot = physics_engine.Slingshot(200, height - 200, 30, 200)

        birds[0].load(slingshot)

        mouse_click = False
        flag = 1

        pigs_to_remove = []
        blocks_to_remove = []

        score_text = interface.Label(50, 10, 100, 50, None, self.color['background'])
        score_text.add_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        birds_remaining = interface.Label(120, 50, 100, 50, None, self.color['background'])
        birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        pigs_remaining = interface.Label(110, 90, 100, 50, None, self.color['background'])
        pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))

        mandav = interface.Label(width - 270, height + ground - 70, 300, 100, None, self.color['background'])
        mandav.add_text("MANDAV", 60, "Fonts/arfmoochikncheez.ttf", ( 113, 125, 126 ))

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        self.draw_map()
                    if event.key == pygame.K_p:
                        self.pause()
                    if event.key == pygame.K_ESCAPE:
                        self.pause()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if birds[0].mouse_selected():
                        mouse_click = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_click = False
                    if birds[0].mouse_selected():
                        flag = 0

            if (not birds[0].loaded) and all_rest(pigs, birds, blocks):
                print("LOADED!")
                birds.pop(0)
                if self.check_win(pigs, birds) == 1:
                    self.score += len(birds)*100
                    self.level_cleared()
                elif self.check_win(pigs,birds) == 0:
                    self.level_failed()

                if not birds == []:
                    birds[0].load(slingshot)
                flag = 1

            if mouse_click:
                birds[0].reposition(slingshot, mouse_click)

            if not flag:
                birds[0].unload()

            #display.fill(self.color['background'])
            color = self.color['background']
            for i in range(3):
                color = (color[0] + 5, color[1] + 5, color[2] + 5)
                pygame.draw.rect(display, color, (0, i*300, width, 300))

            pygame.draw.rect(display, (77, 86, 86), (0, height, width, 50))


            slingshot.draw(birds[0])

            for i in range(len(pigs)):
                for j in range(len(blocks)):
                    pig_v, block_v = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude
                    pigs[i], blocks[j], result_block_pig = physics_engine.collision_handler(pigs[i], blocks[j], "BALL_N_BLOCK")
                    pig_v1, block_v1 = pigs[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block_pig:
                        if abs(pig_v - pig_v1) > d_velocity:
                            blocks_to_remove.append(blocks[j])
                            blocks[j].destroy()
                        if abs(block_v - block_v1) > d_velocity:
                            pigs_to_remove.append(pigs[i])
                            pigs[i].dead()

            for i in range(len(birds)):
                if not (birds[i].loaded or birds[i].velocity.magnitude == 0):
                    for j in range(len(blocks)):
                        birds_v, block_v = birds[i].velocity.magnitude, blocks[j].velocity.magnitude
                        birds[i], blocks[j], result_bird_block = physics_engine.collision_handler(birds[i], blocks[j], "BALL_N_BLOCK")
                        birds_v1, block_v1 = birds[i].velocity.magnitude, blocks[j].velocity.magnitude

                        if result_bird_block:
                            if abs(birds_v - birds_v1) > d_velocity:
                                if not blocks[j] in blocks_to_remove:
                                    blocks_to_remove.append(blocks[j])
                                    blocks[j].destroy()

            for i in range(len(pigs)):
                pigs[i].move()
                for j in range(i+1, len(pigs)):
                    pig1_v, pig2_v = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    pigs[i], pigs[j], result = physics_engine.collision_handler(pigs[i], pigs[j], "BALL")
                    pig1_v1, pig2_v1 = pigs[i].velocity.magnitude, pigs[j].velocity.magnitude
                    result = True
                    if result:
                        if abs(pig1_v - pig1_v1) > d_velocity:
                            if not pigs[j] in pigs_to_remove:
                                pigs_to_remove.append(pigs[j])
                                pigs[j].dead()
                        if abs(pig2_v - pig2_v1) > d_velocity:
                            if not pigs[i] in pigs_to_remove:
                                pigs_to_remove.append(pigs[i])
                                pigs[i].dead()

                for wall in walls:
                    pigs[i] = wall.collision_manager(pigs[i])

                pigs[i].draw()

            for i in range(len(birds)):
                if (not birds[i].loaded) and birds[i].velocity.magnitude:
                    birds[0].move()
                    for j in range(len(pigs)):
                        bird_v, pig_v = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        birds[i], pigs[j], result_bird_pig = physics_engine.collision_handler(birds[i], pigs[j], "BALL")
                        bird_v1, pig_v1 = birds[i].velocity.magnitude, pigs[j].velocity.magnitude
                        result = True
                        if result_bird_pig:
                            if abs(bird_v - bird_v1) > d_velocity:
                                if not pigs[j] in pigs_to_remove:
                                    pigs_to_remove.append(pigs[j])
                                    pigs[j].dead()

                if birds[i].loaded:
                    birds[i].project_path()

                for wall in walls:
                    birds[i] = wall.collision_manager(birds[i])

                birds[i].draw()

            for i in range(len(blocks)):
                for j in range(i + 1, len(blocks)):
                    block1_v, block2_v = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude
                    blocks[i], blocks[j], result_block = physics_engine.block_collision_handler(blocks[i], blocks[j])
                    block1_v1, block2_v1 = blocks[i].velocity.magnitude, blocks[j].velocity.magnitude

                    if result_block:
                        if abs(block1_v - block1_v1) > d_velocity:
                            if not blocks[j] in blocks_to_remove:
                                blocks_to_remove.append(blocks[j])
                                blocks[j].destroy()
                        if abs(block2_v - block2_v1) > d_velocity:
                            if not blocks[i] in blocks_to_remove:
                                blocks_to_remove.append(blocks[i])
                                blocks[i].destroy()

                blocks[i].move()

                for wall in walls:
                    blocks[i] = wall.collision_manager(blocks[i], "BLOCK")

                blocks[i].draw()

            for wall in walls:
                wall.draw()

            score_text.add_text("SCORE: " + str(self.score), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            score_text.draw()

            birds_remaining.add_text("BIRDS REMAINING: " + str(len(birds)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            birds_remaining.draw()

            pigs_remaining.add_text("PIGS REMAINING: " + str(len(pigs)), 25, "Fonts/Comic_Kings.ttf", (236, 240, 241))
            pigs_remaining.draw()

            mandav.draw()

            pygame.display.update()

            if all_rest(pigs, birds, blocks):
                for pig in pigs_to_remove:
                    if pig in pigs:
                        pigs.remove(pig)
                        self.score += 100

                for block in blocks_to_remove:
                    if block in blocks:
                        blocks.remove(block)
                        self.score += 50

                pigs_to_remove = []
                blocks_to_remove = []

            clock.tick(60)
