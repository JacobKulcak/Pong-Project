# CONSTANTS
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 600
from player import player;

# BALL CLASS
class ball:
    
    # Initialize attributes
    def __init__(self, x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2, radius=20, color=(255,255,255)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.x_speed = high_low_rand(-15,-7,7,15)
        self.y_speed = high_low_rand(-3,-1,1,3)
        self.base_x_speed = self.x_speed
        self.base_y_speed = self.y_speed
        self.friction = 0.99
        self.cooldown = 0
        self.draw()
        
        
    # Update
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
        
        
    # Movement for ball
    def move(self):
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        
        # Slows ball down from gained player momentum
        if (abs(self.x_speed) > abs(self.base_x_speed)):
            self.x_speed *= self.friction
        if (abs(self.y_speed) > abs(self.base_y_speed)):
            self.y_speed *= self.friction
        
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
            self.cooldown = 5
    
    
    # If a ball is colliding with given player, return true
    def rect_circle_collision(self, p):
        closest_x = max(p.left, min(self.x, p.left + p.width))
        closest_y = max(p.top, min(self.y, p.top + p.height))
        
        # Calculate distance from circle's center to this closest point
        distance = math.sqrt((closest_x - self.x) ** 2 + (closest_y - self.y) ** 2)
        
        # Collision occurs if the distance is less than or equal to the circle's radius
        return distance <= self.radius
    
#==========================================================================================================

class button:
    pass

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

#===============================================================================================================

# START SCREEN
def start_screen():
    running = True
    black_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    black_surface.fill((0,0,0))
    black_surface.set_alpha(230)
    
    title_surface = title_font.render(("Ultimate BONG"), True, (20,200,50))
    title_rect = title_surface.get_rect(center = (SCREEN_WIDTH/2, 100))
    
    button_color = (70,130,180)
    start_button = pygame.Rect(400,300,200,100)
    start_text = normal_font.render("START", True, (255,255,255))
    start_text_rect = start_text.get_rect(center = start_button.center)
    start_button_surface = pygame.Surface((start_button.width, start_button.height))
    
    exit_button = pygame.Rect(SCREEN_WIDTH-600,SCREEN_HEIGHT-300,200,100)
    exit_text = normal_font.render("EXIT", True, (255,255,255))
    exit_text_rect = exit_text.get_rect(center = exit_button.center)
    
    while running:
        
        pygame.Surface.fill(screen,(0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            
            if start_button.collidepoint(pygame.mouse.get_pos()):  # Check if click is inside button
                start_button_surface.set_alpha(255)
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                    running = False
                    return "game"
            else:
                start_button_surface.set_alpha(128)
            
            if exit_button.collidepoint(pygame.mouse.get_pos()):  # Check if click is inside button
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                    running = False
                    return "exit"
        
        screen.blit(bob, (0,0))
        screen.blit(black_surface, (0,0))
        screen.blit(title_surface, title_rect)
        screen.blit(start_button_surface, (400,300))
        
        pygame.draw.rect(screen, button_color, start_button)
        screen.blit(start_text, start_text_rect)
        
        pygame.draw.rect(screen, button_color, exit_button)
        screen.blit(exit_text, exit_text_rect)
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            running = False
            return "game"
            
        pygame.display.update()

#=================================================================================================================

# MAIN GAME LOOP
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
            balls.append(ball())
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
player_1.set_borders(0, SCREEN_HEIGHT-200, 0, SCREEN_WIDTH/2 - 21 - player_1.rect.width)

# Set up player 2 with controls and borders
player_2 = player("Player 2", SCREEN_WIDTH*0.75, (SCREEN_HEIGHT/2 - 200/2), 20, 200, (200,200,0))
player_2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
player_2.set_borders(0, SCREEN_HEIGHT-200, SCREEN_WIDTH/2 + 21 ,SCREEN_WIDTH - player_2.rect.width)

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