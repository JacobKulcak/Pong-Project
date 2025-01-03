# Initialize pygame and import libraries
import pygame, sys, math, random
pygame.init()

screen_width, screen_height = 1500, 700

#=========================================================================================================================

class player:
    
    # Init method creates rect and score and draws to screen
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0
        self.color = color
        self.draw()
        
    # Saves attributes for 4-directional movement keys
    def set_controls(self, key_up, key_down, key_left, key_right):
        self.key_up = key_up
        self.key_down = key_down
        self.key_left = key_left
        self.key_right = key_right
        
    # Saves attributes for the player's movement borders
    def set_borders(self, top, down, left, right):
        self.top_border = top
        self.bottom_border = down
        self.left_border = left
        self.right_border = right
    
    # Updates player every frame
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
    # Called if player scores
    def inc_score(self):
        self.score += 1
        
    # Player movement based on movement key and border attributes
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
    
    # Initialize attributes
    def __init__(self, x=screen_width/2, y=screen_height/2, radius=10, color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = random.randint(-20,20)
        self.y_speed = random.randint(-10,10)
        self.draw()
        
    # Update
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
        
    # Movement for ball
    def move(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        
        # Borders
        if (self.x - self.radius) < 0:
            self.x_speed = self.x_speed * -1
            collision_sound.play()
        if (self.x + self.radius) > screen_width:
            self.x_speed = self.x_speed * -1
            collision_sound.play()
        if (self.y - self.radius) < 0:
            self.y_speed = self.y_speed * -1
            collision_sound.play()
        if (self.y + self.radius) > screen_height:
            self.y_speed = self.y_speed * -1
            collision_sound.play()


def rect_circle_collision(p, b_coord, b_rad):
    bx, by = b_coord
    p_x, p_y, p_w, p_h = p
    
    closest_x = max(p_x, min(bx, p_x + p_w))
    closest_y = max(p_y, min(by, p_y + p_h))
    
    # Calculate distance from circle's center to this closest point
    distance = math.sqrt((closest_x - bx) ** 2 + (closest_y - by) ** 2)
    
    # Collision occurs if the distance is less than or equal to the circle's radius
    return distance <= b_rad

#===================================================================================================================
        
# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("bob.png"))

# Set up player 1 with controls and borders
player_1 = player(screen_width*0.25, (screen_height/2 - 200/2), 20, 200, (10,100,250))
player_1.set_controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
player_1.set_borders(0, screen_height-200, 0, screen_width/2 - player_1.rect.width)

# Set up player 2 with controls and borders
player_2 = player(screen_width*0.75, (screen_height/2 - 200/2), 20, 200, (200,200,0))
player_2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player_2.set_borders(0, screen_height-200, screen_width/2 + 2,screen_width - player_2.rect.width)

# Set up ball array
balls = [ball(screen_width/2, screen_height/2, 20, (255,255,255))] 

# Music play
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 1000)

# Create objects for framerate, sound effects and fonts used
collision_sound = pygame.mixer.Sound("BallCollide.mp3")
victory_sound = pygame.mixer.Sound("Victory.mp3")
font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
running = True
waiting_for_release = False

#=========================================================================================================================

# Main game loop
while running:
    
    # When window is closed, program stops
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Events for ball spawn
        if event.type == pygame.KEYDOWN and not waiting_for_release:    
            if event.key == pygame.K_SPACE:
                balls.append(ball())
                waiting_for_release = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                waiting_for_release = False
    
    # Framerate
    clock.tick(60)
    
    # Player movement
    key = pygame.key.get_pressed()
    player_1.move(key); player_2.move(key)
    
    # Escape key close game
    if key[pygame.K_ESCAPE]:
        running = False
    
    # Fill screen with blue
    screen.fill((10, 25, 50))
    
    # Dividing line
    pygame.draw.line(screen, (0,0,0), (screen_width/2,0), (screen_width/2,screen_height), width=2)
    
    # Players and ball update
    player_1.draw(); player_2.draw(); 
    
    # For every ball object
    for b in balls:
        
        # Update and draw new location
        b.move(); b.draw()
        
        # Detects collision between ball and player 1
        if(rect_circle_collision(player_1.rect, (b.x, b.y), b.radius)):
            b.x_speed *= -1
            player_1.inc_score()
            collision_sound.play()
            b.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        # Detects collision between ball and player 2
        if(rect_circle_collision(player_2.rect, (b.x,b.y), b.radius)):
            b.x_speed *= -1
            player_2.inc_score()
            collision_sound.play()
            b.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
    # Player 1 scoreboard
    text_surface = font.render(str(player_1.score), True, (20,200,50))
    screen.blit(text_surface, (screen_width*0.25,50))
    
    # Player 2 scoreboard
    text_surface = font.render(str(player_2.score), True, (200,20,30))
    screen.blit(text_surface, (screen_width*0.75,50))
    
    # Victory Check
    if player_1.score == 1000 or player_2.score == 1000:
        victory_sound.play()
        running = False
        
    # Update the display
    pygame.display.update()

# END GAME LOOP
#===============================================================================================================

# Quit Pygame
pygame.quit()
sys.exit()

#===============================================================================================================