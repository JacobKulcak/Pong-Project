import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load('bob.png'))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill((0, 0, 255))  # RGB color: blue

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
