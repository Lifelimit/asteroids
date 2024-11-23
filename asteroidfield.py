import pygame
import random
from asteroids import Asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    # Define spawn edges - each has a direction and position function
    edges = [
        # Right edge
        [pygame.Vector2(-1, 0), lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],
        # Left edge  
        [pygame.Vector2(1, 0), lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT)],
        # Bottom edge
        [pygame.Vector2(0, -1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS)],
        # Top edge
        [pygame.Vector2(0, 1), lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS)]
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.current_spawn_rate = ASTEROID_SPAWN_RATE

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt, score):
        self.spawn_timer += dt
        
        # Faster spawn rate as score increases
        spawn_rate = max(ASTEROID_SPAWN_RATE / (1 + score/300), ASTEROID_MIN_SPAWN_RATE)
        
        if self.spawn_timer > spawn_rate:
            self.spawn_timer = 0
            
            # Pick random edge and position
            edge = random.choice(self.edges)
            pos = edge[1](random.random())
            
            # Calculate velocity based on score
            speed = random.randint(30, 80) * (1 + score/250)
            vel = edge[0] * speed
            vel = vel.rotate(random.randint(-30, 30))
            
            # Spawn asteroid
            size = random.randint(1, ASTEROID_KINDS) * ASTEROID_MIN_RADIUS
            self.spawn(size, pos, vel)