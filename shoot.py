import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.should_constrain = False
                
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        super().update(dt)
        self.check_bounds()
        
    def check_bounds(self):
        # Kill the shot if it goes off screen
        if (self.position.x < 0 or 
            self.position.x > SCREEN_WIDTH or 
            self.position.y < 0 or 
            self.position.y > SCREEN_HEIGHT):
            self.kill()
        