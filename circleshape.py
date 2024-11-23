import pygame
from constants import *

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
            
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.should_constrain = True
        
    def collission(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
        
    
    def draw(self, screen):
        # sub-classes must override
        pass
    
    def update(self, dt):
        self.position += self.velocity * dt
        if self.should_constrain:
            self.constrain_to_screen()
        
    def constrain_to_screen(self):
        if self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.x > SCREEN_WIDTH - self.radius:
            self.position.x = SCREEN_WIDTH - self.radius 
            self.velocity.x *= -1

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -1
        elif self.position.y > SCREEN_HEIGHT - self.radius:
            self.position.y = SCREEN_HEIGHT - self.radius
            self.velocity.y *= -1