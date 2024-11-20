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

#load background music
bg_music = pygame.mixer.Sound('Cullen_pygame/Sax_jingles/jingles_SAX03.ogg')
bg_music.play(-1) # loops = -1

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
plane_alive = True


# Score
lives = [3]
lives_font = pygame.font.Font('Cullen_pygame/Fonts/Kenney_Pixel.ttf', size=45)


# Welcome Screen 
def display_instructions():
    screen.fill((0,0,0)) # Creates a black screen
    font = pygame.font.Font('Cullen_pygame/Fonts/Kenney_Pixel.ttf', 55)

    # Instructions
    instructions = ['Welcome to Flappy Plane', 'Instructions:', 'Press SPACE to move up and down', 'Good Luck!', "Press 'Enter' to continue"]

    for k, v in  enumerate(instructions):  # Error gave me 'Cannot unpack non-iterable int'
        text = font.render(v, True, (173,216,230)) # Light blue text
        screen.blit(text, (50, 50 + k * 60 )) # Centers text, and makes line spacing 60 pixels between lines

    pygame.display.flip() 

# Calling Display Instructions
display_instructions()

# Keys for Next Screen 
click_enter = True 
while click_enter: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 
            pass
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RETURN:
                click_enter = False 


# Main Game
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

    if plane_alive: 
        # Scroll the background
        scroll_background(2) # Speed is 2

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
    
        # Draw Text 
        lives_text = f"Lives: {lives[0]}"  # What prints on screen
        lives_surface = lives_font.render(lives_text, True, (127,0,255)) # Font, and Color (purple)
        lives_rect = lives_surface.get_rect() 
        lives_rect.topleft = (0,0)
        screen.blit(lives_surface, lives_rect)
    
        # Moving plane 
        plane.move(plane_moving_up)

        # Draw the plane
        plane.draw()

        # Check for crash 
        if plane.has_crashed(screen):
            print('DEAD')
            plane_alive = False
            game_running = False
            

        # Flip the display 
        pygame.display.flip()

    #if not plane_alive: 
        # Ending Screen with 'Game Over'
        
        
    clock.tick(60)  

pygame.quit()

