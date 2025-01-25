# BALL CLASS
import pygame, random, math
from utils.functions import *
from utils.constants import *
class Ball:
    
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