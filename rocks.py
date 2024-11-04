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


max_height = 250  # Set the maximum height for the rocks
top_rocks = []  # List for upside-down rocks at the top
bottom_rocks = []  # List for regular rocks at the bottom


def create_top_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(100, max_height)
    
    # Scale the upside-down rock image
    rock_grass_scaled = pygame.transform.scale(down_rock_grass, (rock_width, rock_height))
    rock_x = random.randint(0, WIDTH - rock_width)
    rock_y = 0  # Set y position to 0 for the top of the screen
    speed = random.uniform(1, 3)
    direction = random.choice([-1, 1])  # Random direction: left or right
    return (rock_grass_scaled, rock_x, rock_y, speed, direction)

def create_bottom_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(100, max_height)
    
    # Scale the regular rock image
    rock_grass_scaled = pygame.transform.scale(rock_grass, (rock_width, rock_height))
    rock_x = random.randint(0, WIDTH - rock_width)
    rock_y = HEIGHT - rock_height  # Position at the bottom of the screen
    speed = random.uniform(1, 3)  # Assign speed for horizontal movement
    direction = random.choice([-1, 1])  # Random direction: left or right
    return (rock_grass_scaled, rock_x, rock_y, speed, direction)

# Initial rock creation
for _ in range(5):  # Create 5 top rocks and 5 bottom rocks
    top_rocks.append(create_top_rock())
    bottom_rocks.append(create_bottom_rock())

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
    
    # Adding top rocks
    new_top_rocks = []
    for rock_grass_scaled, rock_x, rock_y, speed, direction in top_rocks:
        rock_x += speed * direction  # Move rock horizontally
        
        # Check for off-screen rocks
        if 0 <= rock_x <= WIDTH:
            new_top_rocks.append((rock_grass_scaled, rock_x, rock_y, speed, direction))
            screen.blit(rock_grass_scaled, (rock_x, rock_y))

    top_rocks = new_top_rocks  # Update the list of top rocks
    
    # Adding bottom rocks
    new_bottom_rocks = []
    for rock_grass_scaled, rock_x, rock_y, speed, direction in bottom_rocks:
        rock_x += speed * direction  # Move rock horizontally
        
        # Check for off-screen rocks
        if 0 <= rock_x <= WIDTH:
            new_bottom_rocks.append((rock_grass_scaled, rock_x, rock_y, speed, direction))
            screen.blit(rock_grass_scaled, (rock_x, rock_y))  # Draw bottom rocks

    bottom_rocks = new_bottom_rocks  # Update the list of bottom rocks

    # Create new rocks at random intervals
    if random.random() < 0.03:  # 1% chance to create a new top rock each frame
        top_rocks.append(create_top_rock())
    if random.random() < 0.03:  # 1% chance to create a new bottom rock each frame
        bottom_rocks.append(create_bottom_rock())


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()