import pygame
import sys
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroids import Asteroid
from shoot import Shot
from explosion import Explosion

def main():
    # Initialize game
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Game state
    score = 0
    lives = 3
    shields = 0
    last_life_bonus = 0
    last_shield_bonus = 0

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set up sprite containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    # Create player and asteroid field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    while True:
        # Handle quit event
        if pygame.event.get(pygame.QUIT):
            return

        # Basic frame setup
        screen.fill("black")
        dt = clock.tick(60) / 1000

        # Draw UI
        score_text = font.render(f"Score: {score}", True, "white")
        lives_text = font.render(f"Lives: {lives}  Shield: {shields}", True, "white")
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH / 2, 20)))

        # Handle bonuses
        if score // 200 > last_life_bonus:
            lives += 1
            last_life_bonus = score // 200
            
        if score >= 500 and (score - 500) // 150 > last_shield_bonus:
            shields += 1
            last_shield_bonus = (score - 500) // 150

        # Update all objects
        for obj in updatable:
            if isinstance(obj, (AsteroidField, Player)):
                obj.update(dt, score)
            else:
                obj.update(dt)

        # Handle collisions
        for asteroid in asteroids:
            # Player collision
            if asteroid.collission(player) and not player.is_immune:
                Explosion(player.position.x, player.position.y, num_particles=30)
                Explosion(asteroid.position.x, asteroid.position.y)
                asteroid.kill()

                if shields > 0:
                    shields -= 1
                else:
                    lives -= 1
                    if lives <= -1:
                        print("Game over!")
                        sys.exit()
                    else:
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity = pygame.Vector2(0, 0)
                        player.current_speed = 0
                        if score < 1000:
                            player.start_immunity()

            # Shot collision
            for shot in shots:
                if asteroid.collission(shot):
                    Explosion(asteroid.position.x, asteroid.position.y)
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 1
                    asteroid.split(asteroidfield)
                    shot.kill()

        # Draw everything
        for obj in drawable:
            if isinstance(obj, Player):
                obj.draw(screen, shields)
            else:
                obj.draw(screen)

        pygame.display.flip()

print("Starting asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()