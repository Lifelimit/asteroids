# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroids import Asteroid
from shoot import Shot

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, 36)
	dt = 0
	score = 0
	lives = 3
 
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
	asteroids = pygame.sprite.Group()
	shots = pygame.sprite.Group()
 
	Player.containers = (updatable, drawable)
	Asteroid.containers = (asteroids, updatable, drawable)
	AsteroidField.containers = (updatable)
	Shot.containers = (shots, updatable, drawable)
 
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
	asteroidfield = AsteroidField()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black") # fill the screen with black
		dt = clock.tick(60) / 1000 # limit fps to 60
  
		score_text = font.render(f"Score: {score}", True, pygame.Color("white"))
		text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 20))
		screen.blit(score_text, text_rect)
  
		lives_text = font.render(f"Lives: {lives}", True, pygame.Color("white"))
		text_rect = lives_text.get_rect(center=(50, 20))
		screen.blit(lives_text, text_rect)

		for object in updatable:
			object.update(dt)
		
		for asteroid in asteroids:
			if asteroid.collission(player):
				lives -= 1
				if lives <= -1:
					print("Game over!")
					sys.exit()
				else:
					player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
					player.velocity = pygame.Vector2(0, 0)
     
    
			for shot in shots:
				if asteroid.collission(shot):
					if asteroid.radius <= ASTEROID_MIN_RADIUS:
						score += 1
					asteroid.split(asteroidfield)
					shot.kill()
					
    
		for object in drawable:
			object.draw(screen)
		
		pygame.display.flip()

print("Starting asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
	main()