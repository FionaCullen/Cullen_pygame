# Example file showing a basic pygame "game loop"
import pygame
import math 

# pygame setup
pygame.init()
WIDTH = 800 
HEIGHT = 480 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


# BUILD THE BACKGROUND WITH TILES
background = pygame.Surface((WIDTH,HEIGHT))
background.fill((255,0,0))

# load tile images to variables
sky = pygame.image.load('PNG/background.png')     
grass = pygame.image.load('PNG/groundGrass.png')
# get to the tile_size
TILE_SIZE = sky.get_width()

background.blit(sky, (0,0))
grass_y = HEIGHT-grass.get_height()
background.blit(grass, (0,grass_y))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with background
    screen.blit(background, (0,0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()