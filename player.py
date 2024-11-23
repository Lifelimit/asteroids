import pygame
from constants import *
from circleshape import CircleShape
from shoot import Shot
from explosion import Explosion

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.current_speed = 0
        self.is_immune = False
        self.immunity_timer = 0
    
    def triangle(self):
        forward = pygame.Vector2(0,1).rotate(self.rotation)
        right = pygame.Vector2(0,1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen, shields=0):
        color = "blue" if shields > 0 and self.is_immune and int(self.immunity_timer * 10) % 2 == 0 else \
                "gray" if self.is_immune and int(self.immunity_timer * 10) % 2 == 0 else "white"
        pygame.draw.polygon(screen, color, self.triangle(), 2)
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
            
    def update(self, dt, score=0):
        super().update(dt)
        self.timer -= dt
        
        if self.is_immune:
            self.immunity_timer -= dt
            if self.immunity_timer <= 0:
                self.is_immune = False
        
        keys = pygame.key.get_pressed()
        
        if not (keys[pygame.K_w] or keys[pygame.K_s]):
            self.velocity = pygame.Vector2(0, 0)
            self.current_speed = 0
        
        if keys[pygame.K_a]: self.rotate(-dt)
        if keys[pygame.K_d]: self.rotate(+dt)
        if keys[pygame.K_w]: self.thrust_forward(dt)
        if keys[pygame.K_s]: self.thrust_backward()
        if keys[pygame.K_SPACE]: self.shoot(score)
            
    def thrust_forward(self, dt):
        self.current_speed = min(self.current_speed + PLAYER_ACCELERATION * dt, PLAYER_MAX_SPEED)
        self.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * self.current_speed
        
    def thrust_backward(self):
        self.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SPEED
        
    def shoot(self, score):
        if self.timer <= 0:
            if score >= 1000:
                cooldown = 0.025
                shots = 10
            elif score >= 500:
                cooldown = 0.1 - (0.075 * (score - 500) / 500)
                shots = 10
            elif score >= 400: cooldown, shots = 0.15, 9
            elif score >= 300: cooldown, shots = 0.2, 8
            elif score >= 200: cooldown, shots = 0.25, 7
            elif score >= 150: cooldown, shots = 0.3, 6
            elif score >= 100: cooldown, shots = 0.35, 5
            elif score >= 50: cooldown, shots = 0.4, 3
            elif score >= 20: cooldown, shots = 0.45, 2
            else: cooldown, shots = 0.5, 1
            
            self.shoot_pattern(shots)
            self.timer = cooldown
            
    def shoot_pattern(self, num_shots):
        if num_shots == 1:
            angles = [0]
        elif num_shots == 2:
            angles = [-10, 10]
        elif num_shots == 3:
            angles = [-15, 0, 15]
        elif num_shots == 5:
            angles = [-20, -10, 0, 10, 20]
        elif num_shots == 6:
            angles = [-25, -15, -5, 5, 15, 25]
        elif num_shots == 7:
            angles = [-30, -20, -10, 0, 10, 20, 30]
        elif num_shots == 8:
            angles = [-35, -25, -15, -5, 5, 15, 25, 35]
        elif num_shots == 9:
            angles = [-40, -30, -20, -10, 0, 10, 20, 30, 40]
        else:  # 10 shots
            angles = [-45, -35, -25, -15, -5, 5, 15, 25, 35, 45]
            
        for angle in angles:
            self.create_shot(angle)
            
    def create_shot(self, angle_offset):
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation + angle_offset) * PLAYER_SHOOT_SPEED
    
    def start_immunity(self, shield_hit=False):
        self.is_immune = True
        self.immunity_timer = SHIELD_IMMUNITY_TIME if shield_hit else PLAYER_IMMUNITY_TIME