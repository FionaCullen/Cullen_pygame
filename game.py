import pygame
import random
from rock import Rock
from plane import Plane

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

# Initalizing Plane 
plane = Plane(WIDTH = 800, HEIGHT = 480, screen = screen)

# Get tile size
TILE_SIZE = sky.get_width()
background.blit(sky, (0, 0))
grass_y = HEIGHT - grass.get_height()
background.blit(grass, (0, grass_y))

rock_creation_time = 0 # Keeping track of how much time has passed since the last rock was created (This is to ensure that no rocks get created over top one another)
rock_creation_interval = 650  # Interval for rock creation (A rock will be created every 0.65 seconds)
top_rocks = []     # Upside-down rocks at the top (Initalizing)
bottom_rocks = []  # Regular rocks at the bottom (Initalizing)

def scroll_background(speed): 
    global background_x
    background_x -= speed # Background moves left, making it look like the plane is moving forward
    if background_x <= -WIDTH: # If the background has moved completely off the screen, reset it
        background_x = 0  # This is the reset so that the screen looks like it never ends.

# initializing plane movement and if has crashed or not 
plane_moving_up = False 

# keys
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN: # checks if key is pressed 
            if event.key == pygame.K_SPACE: # if yes, upward movement 
                plane_moving_up = True  
        elif event.type == pygame.KEYUP: # checks if key is released 
            if event.key == pygame.K_SPACE: # if yes, no upward movement 
                plane_moving_up = False 

    # Scroll the background
    scroll_background(2) # Speed is 2

    # Crash
    r,g,b,_= screen.get_at(???) # Setting where the pixel colors are 

    if r in range(230,240) and g in range(240,250) and b in range(245,255): 
        pass
    else: 
        plane_alive = False # Since I am not using sprites I need to use this in order to have my plane crash and get removed


    # Fill the screen with background
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + WIDTH, 0))

    # Update the timer for rock creation
    rock_creation_time += clock.get_time() # rock_creation_time keeps track how much time has passed since the rock was created and clock keeps track of the time that two frames have been created
        # (Controlling the time when new rocks appear)

    # Create new rocks
    if rock_creation_time >= rock_creation_interval: # If it is greater or equal to- it is time to create a new rock
        if random.random() < 0.3:  # 30 p ercent chance a rock will be created. Generates a random number, and if it below 0.3 it will create a rock.
            # (Changing this changes the speed at which rocks appear on the screen)
            top_rock = Rock(top_rock= True, screen = screen, WIDTH = WIDTH, HEIGHT = HEIGHT) # Upside down rock is created 
            top_rocks.append(top_rock) # Added to the list, which keeps track of all rocks in the game
        if random.random() < 0.3:  # 30 percent chance a rock will be created. Generates a random number, and if it below 0.3 it will create a rock.
            # (Changing this changes the speed at which rocks appear on the screen)
            bottom_rock = Rock(top_rock= False, screen = screen, WIDTH = WIDTH, HEIGHT = HEIGHT) # Bottom screen rocks are created
            bottom_rocks.append(bottom_rock) # Added to the list, which keeps track of all rocks in the game
            
        rock_creation_time = 0  # After creating a rock it resets to the timer to zero so it can create more rocks

    # Move rocks on and off the screen
    new_top_rocks = []
    for rock in top_rocks: 
        if not rock.offscreen(): 
            new_top_rocks.append(rock)
    top_rocks = new_top_rocks

    new_bottom_rocks = []
    for rock in bottom_rocks: 
        if not rock.offscreen():
            new_bottom_rocks.append(rock)
    bottom_rocks = new_bottom_rocks

    # Move rocks on the screen
    for rock in top_rocks + bottom_rocks: 
        rock.move(2)
   
    # Draw top rocks
    for rock in top_rocks + bottom_rocks: 
        rock.draw()
    
    
    # Moving plane 
    plane.move(plane_moving_up)

    # Draw the plane
    plane.draw()

    # Flip the display 
    pygame.display.flip()

    clock.tick(60)  

pygame.quit()

