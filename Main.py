# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1800, 700

# PLAYER CLASS
class player:
    
    # Init method creates rect and score and draws to screen
    def __init__(self, name, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.score = 0
        self.color = color
        self.x_velocity = 0
        self.y_velocity = 0
        self.acceleration = 0.8
        self.friction = 0.88
        self.max_speed = 10
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
        
        # For any given movement key being pushed, apply acceleration on current velocity every frame
        if (key[self.key_up]):
            self.y_velocity -= self.acceleration
        if (key[self.key_down]):
            self.y_velocity += self.acceleration
        if (key[self.key_left]):
            self.x_velocity -= self.acceleration
        if (key[self.key_right]):
            self.x_velocity += self.acceleration
        
        
        # If neither horizontal key is pushed, apply friction to velocity
        # If velocity is low enough, set velocity to 0 to prevent unnecessary computations
        if not key[self.key_left] and not key[self.key_right]:
            if abs(self.x_velocity) >= 0.1:
                self.x_velocity *= self.friction
            if abs(self.x_velocity) < 0.1:
                self.x_velocity = 0


        # Same as above for vertical keys
        if not key[self.key_up] and not key[self.key_down]:
            if abs(self.y_velocity) > 0.1:
                self.y_velocity *= self.friction
            if abs(self.y_velocity) < 0.1:
                self.y_velocity = 0
                
                
        # Prevents velocity from going over a certain limit
        if self.x_velocity > self.max_speed:
            self.x_velocity = self.max_speed
        elif self.x_velocity < -self.max_speed:
            self.x_velocity = -self.max_speed
        if self.y_velocity > self.max_speed:
            self.y_velocity = self.max_speed
        elif self.y_velocity < -self.max_speed:
            self.y_velocity = -self.max_speed
            
        # MAYBE FIX
        # Only apply velocity to position if player is within its borders
        if(self.rect.top > self.top_border) and (self.rect.top < self.bottom_border):
            self.rect.y += self.y_velocity
        else:
            # Otherwise change direction and then apply velocity 
            self.y_velocity *= -1
            self.rect.y += self.y_velocity
            
        # Same as above for horizontal keys   
        if(self.rect.left > self.left_border) and (self.rect.left < self.right_border):
            self.rect.x += self.x_velocity
        else:
            self.x_velocity *= -1
            self.rect.x += self.x_velocity
        
    # Prints player's current score to given coords
    def print_score(self,color,coord):
        text_surface = normal_font.render(str(self.score), True, color)
        screen.blit(text_surface, coord)
           
#========================================================================================================

# BALL CLASS
class ball:
    
    # Initialize attributes
    def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, radius=20, color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = 3#high_low_rand(-20,-5,5,20)
        self.y_speed = 3#high_low_rand(-10,-3,3,10)
        self.draw()
        
        
    # Update
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
        
        
    # Movement for ball
    def move(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        
        # If ball hits left wall, delete self and give player 2 a point
        if (self.x) < 0:
            balls.remove(self)
            collision_sound.play()
            player_2.inc_score()
        # If ball hits right wall, delete self and give player 1 a point
        elif (self.x) > SCREEN_WIDTH:
            balls.remove(self)
            player_1.inc_score()
            collision_sound.play()
        # If ball hits top or bottom wall, reverse vertical velocity
        elif ((self.y - self.radius) < 0) or ((self.y + self.radius) > SCREEN_HEIGHT):
            self.y_speed = self.y_speed * -1
            collision_sound.play()
           
    # PROBLEMATIC
    # Responsible for player/ball collision handling
    def check_col(self, p):
        # If ball collides with player
        if(self.rect_circle_collision(p.rect)):
            # And if ball vertical position is detected to be higher or lower than player position
            if (self.y > p.rect.top + p.rect.height) or (self.y <= p.rect.y):
                # Save player current velocity for later
                player_collision_speed = p.y_velocity
                # Apply ball velocity to player for knockback
                p.y_velocity += self.y_speed
                # Reverse ball velocity
                self.y_speed *= -1
                # Apply initial player speed to ball depending on velocity direction
                if(self.y_speed < 0):
                    self.y_speed -= abs(player_collision_speed)
                elif (self.y_speed >= 0):
                    self.y_speed += abs(player_collision_speed)
                    
            # If ball is on same relative vertical positioning as player, apply above but for x velocity
            else:
                player_collision_speed = p.x_velocity
                p.x_velocity += self.x_speed
                self.x_speed *= -1
                if(self.x_speed < 0):
                    self.x_speed -= abs(player_collision_speed)
                elif (self.x_speed >= 0):
                    self.x_speed += abs(player_collision_speed)

            # Play sound and change color upon colliding with player
            collision_sound.play()
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    
    
    # If a ball is colliding with given player, return true
    def rect_circle_collision(self, p):
        closest_x = max(p.left, min(self.x, p.left + p.width))
        closest_y = max(p.top, min(self.y, p.top + p.height))
        
        # Calculate distance from circle's center to this closest point
        distance = math.sqrt((closest_x - self.x) ** 2 + (closest_y - self.y) ** 2)
        
        # Collision occurs if the distance is less than or equal to the circle's radius
        return distance <= self.radius
    
#==========================================================================================================

# FUNCTIONS

# Pick random value between two given ranges
def high_low_rand(ll, lh, hl, hh):
    if random.choice([True, False]):
        return random.randint(ll, lh)
    else:
        return random.randint(hl, hh)
    
def victory(winner):
    running = True
    victory_sound.play()
    
    text_surface = title_font.render(winner.name + " WINS!!!", True, (255,255,255))
    screen.blit(text_surface, (SCREEN_WIDTH,SCREEN_HEIGHT))
    
    while running:
        
        key = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (key[pygame.K_ESCAPE]):
                running = False
                return "exit"
            
        if (key[pygame.K_SPACE]):
            return "start"

#===============================================================================================================

# START SCREEN
def start_screen():
    running = True
    while running:
        pygame.Surface.fill(screen,(0,0,0), rect=None, special_flags=0)
        
        screen.blit(bob, (0,0))

        text_surface = title_font.render(("Ultimate BONG"), True, (20,200,50))
        screen.blit(text_surface, (SCREEN_WIDTH*0.25,50))
                
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            running = False
            return "game"
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"

#=================================================================================================================

# MAIN GAME LOOP
def game_loop():
    
    running = True
    start_time = pygame.time.get_ticks()
    
    while running:
        
        #print("framerate: " + str(clock.get_fps()), end = '\r')
        
        # Framerate, Counter, Key checker
        clock.tick(60)
        current_time = pygame.time.get_ticks()
        key = pygame.key.get_pressed()
        
        # When window is closed or ESC key pressed, program stops
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (key[pygame.K_ESCAPE]):
                running = False
                return "exit"

        # Timer based ball spawn
        if (current_time - start_time >= 1000):
            balls.append(ball())
            start_time = current_time
        
        # Blue Background and Line through middle
        screen.fill((0, 5, 10))
        pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH/2,0), (SCREEN_WIDTH/2,SCREEN_HEIGHT), width=2)

        # Players and ball update
        player_1.draw(); player_2.draw()
        player_1.move(key); player_2.move(key)
        
        # For every ball, update location/redraw and check collision w/ players
        for b in balls: 
            b.move(); b.draw()
            b.check_col(player_1); b.check_col(player_2)
            
        # Player 1/2 scoreboard
        player_1.print_score((20,200,50), (SCREEN_WIDTH*0.25,50))
        player_2.print_score((200,20,30), (SCREEN_WIDTH*0.75,50))
        
        print("Player 1 y velocity: " + str(round(player_1.y_velocity, 2)) + " | Player 2 y Velocity: " + str(round(player_2.y_velocity, 2)) + "     ", end = "\r")

        # Victory Check NEEDS WORK 
        if player_1.score == 500:
            running = False
            victory(player_1)
        elif player_2.score == 500:
            running = False
            return victory(player_2)
        
        # Update the display
        pygame.display.update()

# END GAME LOOP

#===============================================================================================================

# INITIALIZE
import pygame, sys, math, random
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BOB THE VIDEOGAME")
pygame.display.set_icon(pygame.image.load("Resources/bob.png"))

# Set up player 1 with controls and borders
player_1 = player("Player 1", SCREEN_WIDTH*0.25, (SCREEN_HEIGHT/2 - 200/2), 20, 200, (10,100,250))
player_1.set_controls(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
player_1.set_borders(0, SCREEN_HEIGHT-200, 0, SCREEN_WIDTH/2 - player_1.rect.width)

# Set up player 2 with controls and borders
player_2 = player("Player 2", SCREEN_WIDTH*0.75, (SCREEN_HEIGHT/2 - 200/2), 20, 200, (200,200,0))
player_2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player_2.set_borders(0, SCREEN_HEIGHT-200, SCREEN_WIDTH/2 + 2,SCREEN_WIDTH - player_2.rect.width)

# Set up ball array
balls = [ball(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 20, (255,255,255))] 

# Music play
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.load("Resources/BGM-1.mp3")
pygame.mixer.music.play(-1, 0, 1000)

# Create objects for framerate, sound effects and fonts used
collision_sound = pygame.mixer.Sound("Resources/BallCollide.mp3")
victory_sound = pygame.mixer.Sound("Resources/Victory.mp3")
title_font = pygame.font.Font("Resources/Saphifen.ttf", 154)
normal_font = pygame.font.Font(None, 72)
clock = pygame.time.Clock()
waiting_for_release = False
start_time = pygame.time.get_ticks()
bob = pygame.image.load("Resources/Bob.jpg")
bob = pygame.transform.scale(bob, (SCREEN_WIDTH,SCREEN_HEIGHT))

running = True
current_scene = "start"

#===================================================================================================================
# MAIN LOOP

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

#===============================================================================================================