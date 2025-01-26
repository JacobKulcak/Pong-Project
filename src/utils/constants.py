# CONSTANTS
import pygame
from src.classes.player import Player
from src.classes.ball import Ball

SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 600
collision_sound = pygame.mixer.Sound("resources/BallCollide.mp3")
victory_sound = pygame.mixer.Sound("resources/Victory.mp3")
title_font = pygame.font.Font("resources/Saphifen.ttf", 154)
normal_font = pygame.font.Font(None, 72)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Set up ball array
balls = [Ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 20, (255,255,255))] 

bob = pygame.image.load("resources/Bob.jpg")