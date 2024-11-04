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

rock_creation_time = 0 
rock_creation_interval = 1000
max_height = 250  # Set the maximum height for the rocks
top_rocks = []  # List for upside-down rocks at the top
bottom_rocks = []  # List for regular rocks at the bottom

def create_top_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(10, max_height)
    rock_grass_scaled = pygame.transform.scale(down_rock_grass, (rock_width, rock_height))
    rock_x = random.randint(0, WIDTH - rock_width)
    rock_y = 0  # Top of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def create_bottom_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(10, max_height)
    rock_grass_scaled = pygame.transform.scale(rock_grass, (rock_width, rock_height))
    rock_x = random.randint(0, WIDTH - rock_width)
    rock_y = HEIGHT - rock_height  # Bottom of the screen
    speed = random.uniform(1, 3)  # Speed for horizontal movement
    return (rock_grass_scaled, rock_x, rock_y, speed)

def rocks_overlap(new_rock, existing_rocks):
    """Check if the new rock overlaps with any existing rocks."""
    new_image, new_x, new_y = new_rock
    new_rect = pygame.Rect(new_x, new_y, new_image.get_width(), new_image.get_height())

    for rock in existing_rocks:
        existing_image, existing_x, existing_y = rock
        existing_rect = pygame.Rect(existing_x, existing_y, existing_image.get_width(), existing_image.get_height())
        
        if new_rect.colliderect(existing_rect):
            return True  # There is an overlap
    return False  # No overlap

def try_create_bottom_rock(existing_rocks):
    while True:
        new_rock = create_bottom_rock()
        if not rocks_overlap(new_rock, existing_rocks):
            return new_rock  # Return the new rock if no overlap

def try_create_top_rock(existing_rocks):
    while True: 
        new_rock = create_top_rock()
        if not rocks_overlap(new_rock, existing_rocks):
            return new_rock

def scroll_background(speed): 
    global background_x
    background_x -= speed 
    if background_x <= -WIDTH: 
        background_x = 0  

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scroll_background(2)

    # Fill the screen with background
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + WIDTH, 0))

    # Update the timer for rock creation
    rock_creation_time += clock.get_time()

    # Create new rocks based on the timer
    if rock_creation_time >= rock_creation_interval:
        if random.random() < 0.3:  # Chance to create a new top rock
            top_rocks.append(try_create_top_rock(top_rocks))
        if random.random() < 0.3:  # Chance to create a new bottom rock
            bottom_rocks.append(try_create_bottom_rock(bottom_rocks))
        rock_creation_time = 0  # Reset the timer

    # Update and remove top rocks
    new_top_rocks = []
    for rock in top_rocks: 
        rock_grass_scaled, rock_x, rock_y = rock
        if rock_x > -rock_grass_scaled.get_width(): 
            new_top_rocks.append(rock)

    top_rocks = new_top_rocks 

    # Update and remove bottom rocks
    new_bottom_rocks = []
    for rock in bottom_rocks:
        rock_grass_scaled, rock_x, rock_y, speed = rock
        rock_x -= 2  # Move rock to the left (scrolling effect)
        if rock_x > -rock_grass_scaled.get_width():
            new_bottom_rocks.append((rock_grass_scaled, rock_x, rock_y, speed))

    bottom_rocks = new_bottom_rocks

    # Draw top rocks (stationary)
    for rock in top_rocks:
        screen.blit(rock[0], (rock[1], rock[2]))  # Draw each top rock

    # Draw bottom rocks (moving)
    for rock in bottom_rocks:
        screen.blit(rock[0], (rock[1], rock[2])) 

    # Flip the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)  # Limits FPS to 60

pygame.quit()

