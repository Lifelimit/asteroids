import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
        
    def update(self, dt):
        super().update(dt)
    
    def split(self, asteroidfield):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
            
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        speed = self.velocity.length() * 1.2
        
        for angle in [20, -20]:
            new_velocity = self.velocity.rotate(angle)
            new_velocity.scale_to_length(speed)
            asteroidfield.spawn(new_radius, self.position, new_velocity)
            
        self.kill()