import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600, 800
pX, pY = 0, 0
p2X, p2Y = 1000, 800
sizeX, sizeY = 20, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load('bob.png'))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        pX = pX - 1
    if key[pygame.K_w] == True:
        pY = pY - 1
    if key[pygame.K_s] == True:
        pY = pY + 1
    if key[pygame.K_d] == True:
        pX = pX + 1
    if key[pygame.K_LEFT] == True:
        p2X = p2X - 1
    if key[pygame.K_UP] == True:
        p2Y = p2Y - 1
    if key[pygame.K_DOWN] == True:
        p2Y = p2Y + 1
    if key[pygame.K_RIGHT] == True:
        p2X = p2X + 1

    # Fill the screen with a color
    screen.fill((0, 0, 255))  # RGB color: blue

    pygame.draw.rect(screen, (255,50,50), (pX, pY, sizeX, sizeY))
    pygame.draw.rect(screen, (200,200,0), (p2X, p2Y, sizeX, sizeY))

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
