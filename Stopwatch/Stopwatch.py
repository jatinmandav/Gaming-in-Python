# -------------------------------------------------------------------------------------------
#
# Jatin Kumar Mandav
#
# Stopwatch Using Pygame
# Pause or Unpause : Space Bar or 'p'
# Reset : 'r'
# Quit : 'q'
#
# Website : https://jatinmandav.wordpress.com
# YouTube : https://www.youtube.com/channel/UCdpf6Lz3V357cIZomPwjuFQ?view_as=subscriber
# 
# Facebook : facebook.com/jatinmandav
# Twitter : @jatinmandav
# Gmail : jatinmandav3@gmail.com
#
# -------------------------------------------------------------------------------------------

import pygame
import sys
import time

# Initializing of Pygame
pygame.init()

width = 200
height = 100
display = pygame.display.set_mode((width, height))
pygame.display.set_caption(" ")
clock = pygame.time.Clock()

dark_gray = (23, 32, 42)
white = (230, 230, 230)

seconds = 0
pause = False

# Font and Size
font = pygame.font.SysFont("Times New Roman", 24)

# Close the Window
def close():
    pygame.quit()
    sys.exit()

# Blit time and text to Pygame Window
def showTime():
    hours = seconds/3600
    minutes = (seconds/60)%60
    sec = seconds%60
    
    text = font.render("HH    MM    SS", True, white)
    time = font.render(str(hours).zfill(2) + "     " + str(minutes).zfill(2) + "      " + str(sec).zfill(2), True, white)
    display.blit(text, (10, 10))
    display.blit(time, (13, 40))

# Pause the Stopwatch
def Pause():
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.key == pygame.K_p:
                    stopWatch()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_q:
                    close()

        pauseText = font.render("Paused!", True, white)
        display.blit(pauseText, (10, height - 35))
        
        pygame.display.update()
        clock.tick(60)

# Reset StopWatch
def reset():
    global seconds
    seconds = 0 

# StopWatch
def stopWatch():
    tick = True
    global seconds, pause
    pause = False
    while tick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_p:
                    pause = True
                    Pause()
                if event.key == pygame.K_r:
                    reset()
                if event.key == pygame.K_q:
                    close()

        display.fill(dark_gray)
        showTime()
        seconds += 1

        pygame.display.update()
        clock.tick(1)

stopWatch()

