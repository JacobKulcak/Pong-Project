# MAIN GAME LOOP
import pygame
from src.utils.constants import *
from src.scenes.victory_screen import victory
from src.classes.ball import Ball
from src.utils.players import *


def game_loop():
    
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        
        # Framerate, Counter, Key checker
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        
        # When window is closed or ESC key pressed, program stops
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                running = False
                return "exit"
            
        if (key[pygame.K_ESCAPE]):
            running = False
            return "start"

        # Timer based ball spawn
        if (current_time - start_time >= 2000):
            balls.append(Ball())
            start_time = current_time
        
        # Blue Background and Line through middle
        screen.fill((0, 5, 10))
        pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2-20,0), (SCREEN_WIDTH/2-20,SCREEN_HEIGHT), width=2)
        pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2+20,0), (SCREEN_WIDTH/2+20,SCREEN_HEIGHT), width=2)
        pygame.draw.circle(screen, (255,255,255), (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), 20, width=2)

        # Ball meter
        pygame.draw.line(screen, (0,250,50), (SCREEN_WIDTH/2-75,SCREEN_HEIGHT - 100), (SCREEN_WIDTH/2+75 - (150 * ((current_time - start_time)/2000)), SCREEN_HEIGHT - 100), width=4)

        # Players and ball update
        player_1.draw(); player_2.draw()
        player_1.move(key); player_2.move(key)
        
        # For every ball, update location/redraw and check collision w/ players
        for b in balls: 
            b.move(); b.draw()
            if (b.cooldown == 0):
                b.check_col(player_1); b.check_col(player_2)
            else:
                b.cooldown -= 1
            
        # Player 1/2 scoreboard
        player_1.print_score((20,200,50), (SCREEN_WIDTH*0.25,50))
        player_2.print_score((200,20,30), (SCREEN_WIDTH*0.75,50))
        
        # Update the display
        pygame.display.update()

        # Victory Check NEEDS WORK 
        if player_1.score == 50:
            running = False
            return victory(player_1)
        elif player_2.score == 50:
            running = False
            return victory(player_2)

# END GAME LOOP