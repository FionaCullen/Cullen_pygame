import pygame
import random

# Pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Background setup
background = pygame.Surface((WIDTH, HEIGHT))
background_x = 0
background.fill((255, 0, 0))

# Load tile images
sky = pygame.image.load('Cullen_pygame/PNG/background.png')
grass = pygame.image.load('Cullen_pygame/PNG/groundGrass.png')
rock_grass = pygame.image.load('Cullen_pygame/PNG/rockGrass.png')
down_rock_grass = pygame.image.load('Cullen_pygame/PNG/rockGrassDown.png')

# Load the plane image and scale it
plane = pygame.image.load('Cullen_pygame/PNG/Planes/planeRed2.png')  # Replace with actual plane image
plane_width, plane_height = plane.get_size()  # Get original dimensions
scale_factor = 0.5  # Scale the plane to 50% of its original size
plane = pygame.transform.scale(plane, (int(plane_width * scale_factor), int(plane_height * scale_factor)))

# Plane initial position (center of the screen horizontally, starting in the middle vertically)
plane_x = WIDTH // 4  # Horizontal position
plane_y = HEIGHT // 2  # Vertical position
plane_speed = 5  # Speed of vertical movement
plane_moving_up = False  # Plane movement direction

# Get tile size
TILE_SIZE = sky.get_width()
background.blit(sky, (0, 0))
grass_y = HEIGHT - grass.get_height()
background.blit(grass, (0, grass_y))

rock_creation_time = 0
rock_creation_interval = 650  # Interval for rock creation
max_height = 260  # Max height for rocks
top_rocks = []     # Upside-down rocks at the top
bottom_rocks = []  # Regular rocks at the bottom

def create_top_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(100, max_height)
    rock_grass_scaled = pygame.transform.scale(down_rock_grass, (rock_width, rock_height))
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = 0  # Top of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def create_bottom_rock():
    rock_width = random.randint(50, 150)
    rock_height = random.randint(100, max_height)
    rock_grass_scaled = pygame.transform.scale(rock_grass, (rock_width, rock_height))
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = HEIGHT - rock_height  # Bottom of the screen
    return (rock_grass_scaled, rock_x, rock_y)

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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                plane_moving_up = True  # Toggle upward movement when spacebar is pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                plane_moving_up = False  # Stop moving up when spacebar is released

    # Scroll the background
    scroll_background(2)

    # Fill the screen with background
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + WIDTH, 0))

    # Update the timer for rock creation
    rock_creation_time += clock.get_time()

    # Create new rocks based on the timer
    if rock_creation_time >= rock_creation_interval:
        if random.random() < 0.3:  # Chance to create a new top rock
            top_rock = try_create_top_rock(top_rocks)
            top_rocks.append(top_rock)
        if random.random() < 0.3:  # Chance to create a new bottom rock
            bottom_rock = try_create_bottom_rock(bottom_rocks)
            bottom_rocks.append(bottom_rock)
        rock_creation_time = 0  # Reset the timer

    # Move rocks off the screen
    new_top_rocks = []
    for rock in top_rocks: 
        rock_grass_scaled, rock_x, rock_y = rock
        rock_x -= 2  # Move the rock to the left along with the screen
        if rock_x + rock_grass_scaled.get_width() > 0:  # Keep rocks within the screen
            new_top_rocks.append((rock_grass_scaled, rock_x, rock_y))

    top_rocks = new_top_rocks 

    new_bottom_rocks = []
    for rock in bottom_rocks:
        rock_grass_scaled, rock_x, rock_y = rock
        rock_x -= 2  # Move the rock to the left along with the screen
        if rock_x + rock_grass_scaled.get_width() > 0:  # Keep rocks within the screen
            new_bottom_rocks.append((rock_grass_scaled, rock_x, rock_y))

    bottom_rocks = new_bottom_rocks

    # Handle plane vertical movement
    if plane_moving_up:  # Only move up if the spacebar is pressed
        plane_y -= plane_speed
    else:
        plane_y += plane_speed  # Otherwise, move it down

    # Prevent plane from going out of bounds vertically
    plane_y = max(0, min(HEIGHT - plane_height, plane_y))  # Stay within screen bounds

    # Draw top rocks (stationary relative to the background)
    for rock in top_rocks:
        screen.blit(rock[0], (rock[1], rock[2]))  # Draw each top rock

    # Draw bottom rocks (stationary relative to the background)
    for rock in bottom_rocks:
        screen.blit(rock[0], (rock[1], rock[2])) 

    # Draw the plane
    screen.blit(plane, (plane_x, plane_y))  # Draw the plane at the current position

    # Flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits FPS to 60

pygame.quit()

