import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 800
player_x, player_y = 0, 0
player2_x, player2_y = 900, 500
bX, bY = width/2, height/2
tX, tY = 1, 1
sizeX, sizeY = 20, 200
bRad = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("bob.png"))
pygame.mixer.music.load("BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 2000)

# Main game loop ===========================================

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player_x = player_x - 1
    if key[pygame.K_w] == True:
        player_y = player_y - 1
    if key[pygame.K_s] == True:
        player_y = player_y + 1
    if key[pygame.K_d] == True:
        player_x = player_x + 1
    if key[pygame.K_LEFT] == True:
        player2_x = player2_x - 1
    if key[pygame.K_UP] == True:
        player2_y = player2_y - 1
    if key[pygame.K_DOWN] == True:
        player2_y = player2_y + 1
    if key[pygame.K_RIGHT] == True:
        player2_x = player2_x + 1
    
    if (bX - bRad) < 0:
        tX = tX * -1
    if (bX + bRad) > width:
        tX = tX * -1
    if (bY - bRad) < 0:
        tY = tY * -1
    if (bY + bRad) > height:
        tY = tY * -1
    
    bX = bX + tX
    bY = bY + tY

    # Fill the screen with a color
    screen.fill((0, 0, 255))  # RGB color: blue
    
    pygame.draw.rect(screen, (255,50,50), (player_x, player_y, sizeX, sizeY))
    pygame.draw.rect(screen, (200,200,0), (player2_x, player2_y, sizeX, sizeY))
    pygame.draw.circle(screen, (255,255,255),(bX, bY), bRad)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()

# End Game Loop ============================================