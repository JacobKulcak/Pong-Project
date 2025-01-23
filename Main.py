# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 600

from classes import Player
from classes import Ball
from classes import Button
from utils   import functions
import pygame, sys, math, random

pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("Resources/bob.png"))

# Set up player 1 with controls and borders
player_1 = Player("Player 1", SCREEN_WIDTH*0.25, (SCREEN_HEIGHT/2 - 200/2), 20, 200, (10,100,250))
player_1.set_controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
player_1.set_borders(0, SCREEN_HEIGHT-200, 0, SCREEN_WIDTH/2 - 21 - player_1.rect.width)

# Set up player 2 with controls and borders
player_2 = Player("Player 2", SCREEN_WIDTH*0.75, (SCREEN_HEIGHT/2 - 200/2), 20, 200, (200,200,0))
player_2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player_2.set_borders(0, SCREEN_HEIGHT-200, SCREEN_WIDTH/2 + 21 ,SCREEN_WIDTH - player_2.rect.width)

# Set up ball array
balls = [Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 20, (255,255,255))] 

# Music play
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("Resources/BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 1000)

# Create objects for framerate, sound effects and fonts used
collision_sound = pygame.mixer.Sound("Resources/BallCollide.mp3")
victory_sound = pygame.mixer.Sound("Resources/Victory.mp3")
title_font = pygame.font.Font("Resources/Saphifen.ttf", 154)
normal_font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
waiting_for_release = False
start_time = pygame.time.get_ticks()
bob = pygame.image.load("Resources/Bob.jpg")
bob = pygame.transform.scale(bob, (SCREEN_WIDTH,SCREEN_HEIGHT))

running = True
current_scene = "start"

#===================================================================================================================
# MAIN LOOP

while running:
    if (current_scene == "start"):
        current_scene = start_screen()
    elif (current_scene == "game"):
        current_scene = game_loop()
    elif (current_scene == "exit"):
        running = False

# Quit Pygame
pygame.quit()
sys.exit()

#===============================================================================================================