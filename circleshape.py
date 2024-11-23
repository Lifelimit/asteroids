import pygame
from constants import *

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super().__init__(self.containers if hasattr(self, "containers") else None)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.should_constrain = True
        
    def collission(self, other):
        return self.position.distance_to(other.position) <= self.radius + other.radius
    
    def draw(self, screen):
        pass
    
    def update(self, dt):
        self.position += self.velocity * dt
        if self.should_constrain:
            self.constrain_to_screen()
        
    def constrain_to_screen(self):
        # Constrain x position
        if self.position.x < self.radius or self.position.x > SCREEN_WIDTH - self.radius:
            self.position.x = min(max(self.position.x, self.radius), SCREEN_WIDTH - self.radius)
            self.velocity.x *= -1

        # Constrain y position  
        if self.position.y < self.radius or self.position.y > SCREEN_HEIGHT - self.radius:
            self.position.y = min(max(self.position.y, self.radius), SCREEN_HEIGHT - self.radius)
            self.velocity.y *= -1