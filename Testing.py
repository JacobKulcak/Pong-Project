import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1500, 700
player_x, player_y = 0, 0
player2_x, player2_y = 900, 500
bX, bY = width/2, height/2
tX, tY = 1.5, 1.5
sizeX, sizeY = 20, 200
bRad = 20
screen = pygame.display.set_mode((width, height))
player_1 = pygame.Rect(player_x, player_y, sizeX, sizeY)
player_2 = pygame.Rect(player2_x, player2_y, sizeX, sizeY)
ball_center = (bX, bY)
player1_score = 0
player2_score = 0
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("bob.png"))
pygame.mixer.music.load("BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 2000)


def rect_circle_collision(p, b_coord, b_rad):
    bx, by = b_coord
    p_x, p_y, p_w, p_h = p
    
    closest_x = max(p_x, min(bx, p_x + p_w))
    closest_y = max(p_y, min(by, p_y + p_h))
    
    # Calculate distance from circle's center to this closest point
    distance = math.sqrt((closest_x - bx) ** 2 + (closest_y - by) ** 2)
    
    # Collision occurs if the distance is less than or equal to the circle's radius
    return distance <= b_rad


# Main game loop ===========================================

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player_1.move_ip(-1, 0)
    if key[pygame.K_w] == True:
        player_1.move_ip(0, -1)
    if key[pygame.K_s] == True:
        player_1.move_ip(0, 1)
    if key[pygame.K_d] == True:
        player_1.move_ip(1, 0)
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
    ball_center = (bX, bY)

    # Fill the screen with a color
    screen.fill((20, 50, 100))  # RGB color: blue
    pygame.draw.line(screen, (255,255,255), (width/2,0), (width/2,height), width=3)
    
    pygame.draw.rect(screen, (255,50,50), player_1)
    pygame.draw.rect(screen, (200,200,0), player_2)
    pygame.draw.circle(screen, (255,255,255), ball_center, bRad)
    
    if(rect_circle_collision(player_1, ball_center, bRad) == True):
        tX *= -1
        
    print(ball_center, end='\r')
        

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()

# End Game Loop ============================================