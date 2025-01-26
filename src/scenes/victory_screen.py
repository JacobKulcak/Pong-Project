#VICTORY SCREEN
import pygame
from src.utils.constants import *

def victory(winner):
    running = True
    victory_sound.play()
    text_surface = title_font.render(winner.name + " WINS!!!", True, (255,255,255))
    text_rect = text_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2 - 100))
    
    while running:
        
        screen.blit(text_surface, text_rect)
        
        key = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (key[pygame.K_ESCAPE]):
                running = False
                return "exit"
            
        if (key[pygame.K_SPACE]):
            return "start"
        
        pygame.display.update()