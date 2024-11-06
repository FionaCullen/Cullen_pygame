# Example file showing a basic pygame "game loop"
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
plane = pygame.transform.scale(plane, (plane.get_width() // 2, plane.get_height() // 2)) # Scale plane to 50 percent

# Plane initial position (center of the screen horizontally, starting in the middle vertically)
plane_x = WIDTH // 4  # Horizontal position
plane_y = HEIGHT // 2  # Vertical position
plane_speed = 3  # Speed of vertical movement
plane_moving_up = False  # Plane is set to not move up, this allows the plane to not continue moving up if the space bar is not touched

# Get tile size
TILE_SIZE = sky.get_width()
background.blit(sky, (0, 0))
grass_y = HEIGHT - grass.get_height()
background.blit(grass, (0, grass_y))

rock_creation_time = 0 # Keeping track of how much time has passed since the last rock was created (This is to ensure that no rocks get created over top one another)
rock_creation_interval = 650  # Interval for rock creation (A rock will be created every 0.65 seconds)
max_height = 260  # Max height for rocks
top_rocks = []     # Upside-down rocks at the top (Initalizing)
bottom_rocks = []  # Regular rocks at the bottom (Initalizing)

def create_top_rock():
    rock_width = random.randint(50, 150) # Generates a random width between 50 and 150
    rock_height = random.randint(100, max_height) # Generates a random height between 100 and the max height given (260)
    rock_grass_scaled = pygame.transform.scale(down_rock_grass, (rock_width, rock_height)) # Scale the rock to the height and width; which are random
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = 0  # Stays at the top of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def create_bottom_rock():
    rock_width = random.randint(50, 150) # Generates a random width between 50 and 150
    rock_height = random.randint(100, max_height) # Generates a random height between 100 and the max height given (260)
    rock_grass_scaled = pygame.transform.scale(rock_grass, (rock_width, rock_height)) # Scale the rock to the height and width; which are random
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = HEIGHT - rock_height  # Stays at the bottom of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def rocks_overlap(new_rock, existing_rocks): # Checking if any new rocks over lap with existing rocks
    new_image, new_x, new_y = new_rock # new_image = the new rock image, new_x = starting x coordinate of the rectangle (new rock), new_y = starting y coordinate of the rectangle (new rock)
    new_rect = pygame.Rect(new_x, new_y, new_image.get_width(), new_image.get_height()) # gives x and y position, width and height of the image 

    for rock in existing_rocks: # For loop goes over every rock that is already exisiting
        existing_image, existing_x, existing_y = rock # A tuple that includes, the x and y position of the existing rock and the image. 
        existing_rect = pygame.Rect(existing_x, existing_y, existing_image.get_width(), existing_image.get_height()) # Creating a Rect for the existing rock, which gives the x and y position and width and height of the image
        
        if new_rect.colliderect(existing_rect): # Checking to see if a new rock overlaps with an exisiting rock
            # colliderect: test if two rectangle overlap 
            return True  # return true if there is an overlap
    return False  # return false if there is no overlap

def try_create_bottom_rock(existing_rocks): # Creates a new bottom rock, and makes sure that the new rock does not overlap an existing rock
    while True: # We need a while loop because we need to find a rock that does not overlap another rock, so it will continue until it is found.
        new_rock = create_bottom_rock() # Calls the function and assigns it to new_rock (which includes x and y position)
        if not rocks_overlap(new_rock, existing_rocks): # This checks if any new rocks over lap with any existing rocks 
            # if there is no overlap, then it will return false, and the not will then turn it true, returning a new rock
            return new_rock  # Return the new rock if no overlap

def try_create_top_rock(existing_rocks): # Creates a new top rock, and makes sure that the new rock does not overlap an exisiting rock
    while True: # We need a while loop because we want it to continue to try and place a rock until there is no overlap with another rock
        new_rock = create_top_rock() # Calls the function and assigns it to new rock (this function includes an x and y poisiton and height and width of the rock)
        if not rocks_overlap(new_rock, existing_rocks): # This checks to make sure that no new rock that is being added overlaps with an already existing rock
            # if there is no overlap, then it will return false, and the NOT will then turn it true, returning a new rock 
            return new_rock # If no overlap it will execute the if statement and return a new rock

def scroll_background(speed): 
    global background_x
    background_x -= speed # Background moves left, making it look like the plane is moving forward
    if background_x <= -WIDTH: # If the background has moved completely off the screen, reset it
        background_x = 0  # This is the reset so that the screen looks like it never ends.

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
    scroll_background(2) # Speed is 2

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
        rock_x -= 2  # Move the rock to the left along with the screen (At the same rate of 2)
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
    plane_y = max(0, min(HEIGHT - max_height, plane_y))  # Stay within screen bounds

    # Draw top rocks (stationary relative to the background)
    for rock in top_rocks:
        screen.blit(rock[0], (rock[1], rock[2]))  # Draw each top rock

    # Draw bottom rocks (stationary relative to the background)
    for rock in bottom_rocks:
        screen.blit(rock[0], (rock[1], rock[2])) 

    # Draw the plane
    screen.blit(plane, (plane_x, plane_y))  # Draw the plane at the current position

    # Flip the display 
    pygame.display.flip()

    clock.tick(60)  

pygame.quit()


