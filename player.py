# PLAYER CLASS
import pygame

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
        pygame.draw.rect(self.screen, self.color, self.rect)
        
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
            self.y_velocity *= -0.6
            self.rect.y += self.y_velocity
            
        # Same as above for horizontal keys   
        if(self.rect.left > self.left_border):
            self.rect.x += self.x_velocity
        elif(self.x_velocity != 0):
            self.x_velocity *= -0.6
            self.rect.x += self.x_velocity
        else:
            self.rect.x += 1
        
        if (self.rect.left < self.right_border):
            self.rect.x += self.x_velocity
        elif(self.x_velocity != 0):
            self.x_velocity *= -0.6
            self.rect.x += self.x_velocity
        else:
            self.rect.x -= 1
        
    # Prints player's current score to given coords
    def print_score(self,color,coord):
        text_surface = normal_font.render(str(self.score), True, color)
        self.screen.blit(text_surface, coord)
           
#========================================================================================================