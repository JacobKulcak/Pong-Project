from src.classes import Player
from src.classes import Ball
from src.classes import Button

from src.utils.functions  import *
from src.utils.constants  import *
from src.scenes.game_loop import *
from src.scenes.start_screen import *

import pygame, sys, math, random

from src.refresh import GameRefresh
GameRefresh()

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