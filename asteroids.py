import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, width=2)
        
    def update(self, dt):
        super().update(dt)
    
    def split(self, asteroidfield):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        random_angle = random.uniform(20, 50)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        asteroidfield.spawn(new_radius, self.position, a)
        Asteroid.velocity = a * 1.2
        asteroidfield.spawn(new_radius, self.position, b)
        Asteroid.velocity = b * 1.2
        