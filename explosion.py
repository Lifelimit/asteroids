import pygame
import random
from constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, num_particles=20):
        super().__init__()
        if hasattr(self, "containers"):
            self.add(self.containers)
            
        self.particles = []
        for _ in range(num_particles):
            # Create particle data as tuples: (position, velocity, lifetime, size)
            angle = random.uniform(0, 360)
            speed = random.uniform(EXPLOSION_MIN_SPEED, EXPLOSION_MAX_SPEED)
            velocity = pygame.Vector2(0, speed).rotate(angle)
            lifetime = random.uniform(0.5, EXPLOSION_PARTICLE_LIFETIME)
            
            particle = (
                pygame.Vector2(x, y),
                velocity, 
                lifetime,
                random.uniform(1, 3)
            )
            self.particles.append([particle[0], particle[1], lifetime, lifetime, particle[3]])

    def update(self, dt):
        # Update each particle and remove dead ones
        alive_particles = []
        for pos, vel, life, init_life, size in self.particles:
            if life > 0:
                pos += vel * dt
                life -= dt
                alive_particles.append([pos, vel, life, init_life, size])
                
        self.particles = alive_particles
        if not self.particles:
            self.kill()

    def draw(self, screen):
        for pos, _, life, init_life, size in self.particles:
            color = int(255 * life/init_life)
            pygame.draw.circle(screen, (color, color, color), pos, size)