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
plane_y =  HEIGHT // 2 # Vertical position
plane_speed = 3  # Speed of vertical movement
plane_moving_up = False  # Plane is set to not move up, this allows the plane to not continue moving up if the space bar is not touched
plane_height = 36 # Got this number by testing to see when the plane would hit the ground, where I wanted it to
height = 73 # height of plane png
width = 88 # width of plane png
plane_rect = pygame.Rect(plane_x, plane_y, width, height) # Used for crash

# Get tile size
TILE_SIZE = sky.get_width()
background.blit(sky, (0, 0))
grass_y = HEIGHT - grass.get_height()
background.blit(grass, (0, grass_y))

rock_creation_time = 0 # Keeping track of how much time has passed since the last rock was created (This is to ensure that no rocks get created over top one another)
rock_creation_interval = 650  # Interval for rock creation (A rock will be created every 0.65 seconds)
max_height = 260 # Max height for rocks
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
        existing_image, existing_x, existing_y = rock # x and y position of the existing rock and the image. 
        existing_rect = pygame.Rect(existing_x, existing_y, existing_image.get_width(), existing_image.get_height()) # Creating a Rect for the existing rock, which gives the x and y position and width and height of the image
        
        if new_rect.colliderect(existing_rect): # Checking to see if a new rock overlaps with an exisiting rock
            # colliderect: test if two rectangle overlap 
            return True  # return true if there is an overlap
    return False  # return false if there is no overlap

def try_create_bottom_rock(existing_rocks): # Creates a new bottom rock, and makes sure that the new rock does not overlap an existing rock
    while True: # We need a while loop because we need to find a rock that does not overlap another rock, so it will continue until it is found.
        new_rock = create_bottom_rock() # Calls the function and assigns it to new_rock (which includes x and y position)
        if not rocks_overlap(new_rock, existing_rocks): # This checks if any new rocks over lap with any existing rocks 
            # if there is no overlap, then it will return false, and then it will then turn it true, returning a new rock
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

plane_alive = True # Setting this as true because I need it to die later (Not using sprites in my code)

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


    # # Scroll the background
    # scroll_background(2) # Speed is 2

    # # Crash
    # r,g,b,_= screen.get_at(plane_rect.center) # Setting where the pixel colors are 

    # if r in range(230,240) and g in range(240,250) and b in range(245,255): 
    #     pass
    # else: 
    #     plane_alive = False # Since I am not using sprites I need to use this in order to have my plane crash and get removed


    # Fill the screen with background
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + WIDTH, 0))

    # Update the timer for rock creation
    rock_creation_time += clock.get_time() # rock_creation_time keeps track how much time has passed since the rock was created and clock keeps track of the time that two frames have been created
        # (Controlling the time when new rocks appear)

    # Create new rocks
    if rock_creation_time >= rock_creation_interval: # If it is greater or equal to- it is time to create a new rock
        if random.random() < 0.3:  # 30 percent chance a rock will be created. Generates a random number, and if it below 0.3 it will create a rock.
            # (Changing this changes the speed at which rocks appear on the screen)
            top_rock = try_create_top_rock(top_rocks) # Upside down rock is created 
            top_rocks.append(top_rock) # Added to the list, which keeps track of all rocks in the game
    if random.random() < 0.3:  # 30 percent chance a rock will be created. Generates a random number, and if it below 0.3 it will create a rock.
            # (Changing this changes the speed at which rocks appear on the screen)
            bottom_rock = try_create_bottom_rock(bottom_rocks) # Bottom screen rocks are created
            bottom_rocks.append(bottom_rock) # Added to the list, which keeps track of all rocks in the game
    rock_creation_time = 0  # After creating a rock it resets to the timer to zero so it can create more rocks

    # Move rocks off the screen
    new_top_rocks = [] # initializing
    for rock in top_rocks: 
        rock_grass_scaled, rock_x, rock_y = rock # has rocks x position, y position, and the image
        rock_x -= 2  # Move the rock to the left along with the screen (At the same rate of 2)
        if rock_x + rock_grass_scaled.get_width() > 0:  # Adding these two things together you get the right most edge of the rock
            # if it is greater than zero that means it is still visible on the screen, if it is less than zero it means it left the screen
            new_top_rocks.append((rock_grass_scaled, rock_x, rock_y)) # If it is still visible on the screen it will add it to the list and update its position

    top_rocks = new_top_rocks # top rocks is being replaced with the contents of new top rocks

    new_bottom_rocks = [] # initializing 
    for rock in bottom_rocks:
        rock_grass_scaled, rock_x, rock_y = rock # has rocks x position, y position, and the image
        rock_x -= 2  # Move the rock to the left along with the screen (At the same rate of 2)
        if rock_x + rock_grass_scaled.get_width() > 0:  # Adding these two things together you get the right most edge of the rock 
            # if it is greater than zero that means it is still visible on the screen, if it is less than zero it means it left the screen 
            new_bottom_rocks.append((rock_grass_scaled, rock_x, rock_y)) # If it is still visible on the screen it will add it to the list and update its position

    bottom_rocks = new_bottom_rocks # bottom rock is being replaced with the contents of new bottom rocks 

    # Plane's vertical movement
    if plane_moving_up:  # Only move up if the spacebar is pressed
        plane_y -= plane_speed # TRUE Space bar was pressed so the plane moves up 
    else:
        plane_y += plane_speed  # FALSE Space bar was not pressed so the plane moves down 

    # Bounds for plane
    if plane_y < 0: # Does not go above the screen 
        plane_y = 0 
    elif plane_y + plane_height > HEIGHT: # Checking if bottom of the plane has left the bottom of the screen
        plane_y = HEIGHT - plane_height # Sets the plan so it stops before the bottom of the screen

    # Draw top rocks
    for rock_image, rock_x, rock_y in top_rocks: # Goes over every rock in top_rocks
        screen.blit(rock_image, (rock_x, rock_y))  # Accessing the first rock in the list, then all the other rocks using x and y positions
                            
    # Draw bottom rocks
    for rock_image, rock_x,rock_y in bottom_rocks: # Goes over every rock in bottom_rocks
        screen.blit(rock_image, (rock_x, rock_y))  # Accessing the first rock in the list, then all the other rocks using x and y positions
                            
    # Draw the plane
    screen.blit(plane, (plane_x, plane_y))  # Draw the plane at the current position

    # Flip the display 
    pygame.display.flip()

    clock.tick(60)  

pygame.quit()



