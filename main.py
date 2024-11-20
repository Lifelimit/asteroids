# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import Player

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	dt = 0
 
	updatable = pygame.sprite.Group()
	drawable = pygame.sprite.Group()
 
	Player.containers = (updatable, drawable)
 
	player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return

		screen.fill("black") # fill the screen with black
		dt = clock.tick(60) / 1000 # limit fps to 60

		for object in updatable:
			object.update(dt)
		for object in drawable:
			object.draw(screen)
		
		pygame.display.flip()

print("Starting asteroids!")
print(f"Screen width: {SCREEN_WIDTH}")
print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
	main()