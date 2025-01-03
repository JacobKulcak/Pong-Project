import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1500, 700
sizeX, sizeY = 20, 200
player_x, player_y = width*0.25, (height/2 - sizeY/2)
player2_x, player2_y = width*0.75, (height/2 - sizeY/2)
bX, bY = width/2, height/2
tX, tY = 7, 5
bRad = 20
ball_color = (255,255,255)
screen = pygame.display.set_mode((width, height))
player_1 = pygame.Rect(player_x, player_y, sizeX, sizeY)
player_2 = pygame.Rect(player2_x, player2_y, sizeX, sizeY)
ball_center = (bX, bY)
player1_score = 0
player2_score = 0
cooldown = 0
clock = pygame.time.Clock()
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("bob.png"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 1000)
collision_sound = pygame.mixer.Sound("BallCollide.mp3")
victory_sound = pygame.mixer.Sound("Victory.mp3")
font = pygame.font.Font(None, 72)

class player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0
        self.color = color
        self.draw()
        
    def set_controls(self, key_up, key_down, key_left, key_right):
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self)
        
    def inc_score(self):
        self.score += 1
        
    def move(self, key):
        if (key[self.key_left]) and (self.rect.left > 0):
            self.move_ip(-5, 0)
        if (key[self.key_up]) and (self.rect.top > 0):
            self.move_ip(0, -5)
        if (key[self.key_down]) and (self.rect.top < height-sizeY):
            self.move_ip(0, 5)
        if (key[self.key_right]) and (self.rect.left < width/2 - sizeX):
            self.move_ip(5, 0)
        
        

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
    
    clock.tick(60)
    
    print(player1_score, end='\r')
    
    key = pygame.key.get_pressed()
    #player_1.move(key); player_2.move(key)
    
    if (key[pygame.K_ESCAPE] == True):
        running = False
    
    if (bX - bRad) < 0:
        tX = tX * -1
        collision_sound.play()
    if (bX + bRad) > width:
        tX = tX * -1
        collision_sound.play()
    if (bY - bRad) < 0:
        tY = tY * -1
        collision_sound.play()
    if (bY + bRad) > height:
        tY = tY * -1
        collision_sound.play()
    
    bX = bX + tX
    bY = bY + tY
    ball_center = (bX, bY)

    # Fill the screen with a color
    screen.fill((10, 25, 50))  # RGB color: blue
    pygame.draw.line(screen, (0,0,0), (width/2,0), (width/2,height), width=2)
    
    
    #pygame.draw.rect(screen, (10,100,250), player_1)
    player_1.draw()
    pygame.draw.rect(screen, (200,200,0), player_2)
    
    pygame.draw.circle(screen, ball_color, ball_center, bRad)
    
    if(cooldown==False):
        if(rect_circle_collision(player_1, ball_center, bRad) == True):
            tX *= -1
            cooldown = 100
            player1_score += 1
            collision_sound.play()
            ball_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        if(rect_circle_collision(player_2, ball_center, bRad) == True):
            tX *= -1
            cooldown = 100
            player2_score += 1
            collision_sound.play()
            ball_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    else:
        cooldown -= 1
        
    text_surface = font.render(str(player1_score), True, (20,200,50))
    screen.blit(text_surface, (width*0.25,50))
    text_surface = font.render(str(player2_score), True, (200,20,30))
    screen.blit(text_surface, (width*0.75,50))
        
    if player1_score == 5 or player2_score == 50:
        pygame.mixer.music.stop()
        victory_sound.play()
        while pygame.mixer.get_busy():
            pygame.event.wait()
        running = False
    
    # Update the display
    pygame.display.update()
    
# Quit Pygame
pygame.quit()
sys.exit()

# End Game Loop ============================================