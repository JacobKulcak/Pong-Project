import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

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
        
    def set_borders(self, top, down, left, right):
        self.top_border = top
        self.bottom_border = down
        self.left_border = left
        self.right_border = right
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def inc_score(self):
        self.score += 1
        
    def move(self, key):
        if (key[self.key_up]) and (self.rect.top > self.top_border):
            self.rect.move_ip(0, -5)
        if (key[self.key_down]) and (self.rect.top < self.bottom_border):
            self.rect.move_ip(0, 5)
        if (key[self.key_left]) and (self.rect.left > self.left_border):
            self.rect.move_ip(-5, 0)
        if (key[self.key_right]) and (self.rect.left < self.right_border):
            self.rect.move_ip(5, 0)
            
class ball:
    def __init__(self, x, y, radius, color, x_speed, y_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.draw()
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
        
    def move(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        
        #borders
        if (self.x - self.radius) < 0:
            self.x_speed = self.x_speed * -1
            collision_sound.play()
        if (self.x + self.radius) > width:
            self.x_speed = self.x_speed * -1
            collision_sound.play()
        if (self.y - self.radius) < 0:
            self.y_speed = self.y_speed * -1
            collision_sound.play()
        if (self.y + self.radius) > height:
            self.y_speed = self.y_speed * -1
            collision_sound.play()

        
# Set up the display
width, height = 1500, 700
sizeX, sizeY = 20, 200
screen = pygame.display.set_mode((width, height))

player_1 = player(width*0.25, (height/2 - sizeY/2), 20, 200, (10,100,250))
player_1.set_controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
player_1.set_borders(0, height-sizeY, 0, width/2 -sizeX)

player_2 = player(width*0.75, (height/2 - sizeY/2), 20, 200, (200,200,0))
player_2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player_2.set_borders(0, height-sizeY, width/2 + 2,width - sizeX)

ball_1 = ball(width/2, height/2, 20, (255,255,255), 15, 5)


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
    
    key = pygame.key.get_pressed()
    player_1.move(key); player_2.move(key)
    
    if (key[pygame.K_ESCAPE] == True):
        running = False
    
    # Fill the screen with a color
    screen.fill((10, 25, 50))  # RGB color: blue
    pygame.draw.line(screen, (0,0,0), (width/2,0), (width/2,height), width=2)
    
    player_1.draw(); player_2.draw(); ball_1.move(); ball_1.draw()
    
    if(cooldown==False):
        if(rect_circle_collision(player_1.rect, (ball_1.x,ball_1.y), ball_1.radius) == True):
            ball_1.x_speed *= -1
            player_1.score += 1
            collision_sound.play()
            ball_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        if(rect_circle_collision(player_2.rect, (ball_1.x,ball_1.y), ball_1.radius) == True):
            ball_1.x_speed *= -1
            player_2.score += 1
            collision_sound.play()
            ball_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    else:
        cooldown -= 1
        
    text_surface = font.render(str(player_1.score), True, (20,200,50))
    screen.blit(text_surface, (width*0.25,50))
    text_surface = font.render(str(player_2.score), True, (200,20,30))
    screen.blit(text_surface, (width*0.75,50))
        
    if player_1.score == 300 or player_2.score == 100:
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