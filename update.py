# Example file showing a basic pygame "game loop"
import pygame
import math 
from plane import Plane
import random
import sys

# pygame setup
pygame.init()
WIDTH = 800 
HEIGHT = 480 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


# BUILD THE BACKGROUND WITH TILES
background = pygame.Surface((WIDTH,HEIGHT))
background_x = 0 
background.fill((255,0,0))

# load tile images to variables
sky = pygame.image.load('Cullen_pygame/PNG/background.png')     
grass = pygame.image.load('Cullen_pygame/PNG/groundGrass.png')
rock_grass = pygame.image.load('Cullen_pygame/PNG/rockGrass.png')
down_rock_grass = pygame.image.load('Cullen_pygame/PNG/rockGrassDown.png')

# get to the tile_size
TILE_SIZE = sky.get_width()
background.blit(sky, (0,0))
grass_y = HEIGHT-grass.get_height()
background.blit(grass, (0,grass_y))

# Add bottom rocks 
rock_height = rock_grass.get_height()
rock_y = HEIGHT - rock_height

max_height = 250 
rocks = []
for _ in range(5):  # Create 10 rocks
    rock_width = random.randint(50, 150)  # Random width between 50 and 150
    rock_height = random.randint(150, max_height)  # Random height between 10 and max_height
    rock_grass_scaled = pygame.transform.scale(rock_grass,(rock_width, rock_height))
    rock_x = random.randint(0, WIDTH - rock_width)  # Random x position
    rock_y = HEIGHT - rock_height  # Position at the bottom
    rocks.append((rock_grass_scaled, rock_x, rock_y))

# Add top rocks 
down_max_height = 250
down_rocks = []
def create_rock():
    down_rock_width = random.randint(50, 150)  # Random width between 50 and 150
    down_rock_height = random.randint(10, down_max_height)  # Random height between 10 and max_height
    
    # Scale the rock image to random width and height
    down_rock_grass_scaled = pygame.transform.scale(down_rock_grass,(down_rock_width, down_rock_height))
    down_rock_x = random.randint(0, WIDTH - down_rock_width)  # Random x position
    down_rock_y = 0  # Set y position to 0 for the top of the screen
    speed = random.uniform(1, 3)  # Random horizontal speed
    direction = random.choice([-1, 1])  # Random direction: left or right
    return (down_rock_grass_scaled, down_rock_x, down_rock_y, speed, direction)
     
for _ in range(5):  # Create 5 rocks initially
    down_rocks.append(create_rock())

def scroll_background(speed): 
    global background_x
    background_x -= speed 
    if background_x <= -WIDTH: 
        background_x = 0  


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scroll_background(2)

    # fill the screen with background
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + WIDTH, 0))
    
    # Add bottom rocks 
    for rock_grass_scaled, rock_x, rock_y in rocks: 
        screen.blit(rock_grass_scaled, (rock_x, rock_y))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()