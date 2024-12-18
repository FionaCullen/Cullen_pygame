import pygame
import random
from rock import Rock
from plane import Plane
from helpers import display_instructions, display_game_over, take_screenshot

# Pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# load background music
bg_music = pygame.mixer.Sound('Cullen_pygame\mp3\Be_Children.mp3')
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

# Initialize rock elements
rock_creation_time = 0        
rock_creation_interval = 500  # Interval for rock creation (A rock will be created every 0.5 seconds)
top_rocks = []     # Initializing Upside-down rocks at the top
bottom_rocks = []  # Initializing Regular rocks at the bottom 

# Scroll Background
def scroll_background(speed): 
    global background_x
    background_x -= speed         # Background moves left
    if background_x <= -WIDTH:    # If the background has moved completely off the screen, reset it
        background_x = 0          # This is the reset so that the screen looks like it never ends.

# initializing plane movement and if has crashed or not 
plane_moving_up = False 
plane_alive = True

# Score
lives = [3] 
lives_font = pygame.font.Font('Cullen_pygame/Fonts/Kenney_Pixel.ttf', size=45)

# Calling Welcome Screen 
display_instructions(screen, WIDTH)

# Keys for Next Screen (WELCOME SCREEN)
click_enter = True
while click_enter: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False 
            pass
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_RETURN: # If 'enter' is pressed, move to the next screen
                click_enter = False 

# Main Game
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN: # checks if key is pressed 
            if event.key == pygame.K_SPACE: # if yes, upward movement 
                plane_moving_up = True 
            elif event.key == pygame.K_p: # If p is pressed, take a screenshot
                take_screenshot(screen) 
        elif event.type == pygame.KEYUP: # checks if key is released 
            if event.key == pygame.K_SPACE: # if yes, no upward movement 
                plane_moving_up = False
    
    # If plane is alive, do all these things...
    if plane_alive: 

        # Scroll the background
        scroll_background(2) # Speed is 2

        # Fill the screen with background
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + WIDTH, 0))

        # Update the timer for rock creation
        rock_creation_time += clock.get_time() # Running timer for the game, beginning at zero
           
        # Create new rocks
        if rock_creation_time >= rock_creation_interval: # If the running timer is greater than 500, create a new rock on the screen
            if random.random() < 0.3:  # 30 percent chance a rock will be created (random.random generates a number between 0 and 1) 
                top_rock = Rock(top_rock= True, screen = screen, WIDTH = WIDTH, HEIGHT = HEIGHT)
                top_rocks.append(top_rock) # Added to the list
            if random.random() < 0.3:  # 30 percent chance a rock will be created (This is necessary so that there are not rocks being created every 0.5 sec)
                bottom_rock = Rock(top_rock= False, screen = screen, WIDTH = WIDTH, HEIGHT = HEIGHT)
                bottom_rocks.append(bottom_rock) # Added to the list
            
            rock_creation_time = 0  # After creating a rock it resets to the timer to zero
        
        # Removing rocks from the list once they are off the screen
        for rock in top_rocks[:]:
            if rock.offscreen():
                top_rocks.remove(rock)

        for rock in bottom_rocks[:]:
            if rock.offscreen():
                bottom_rocks.remove(rock)

        # Move rocks on the screen
        for rock in top_rocks + bottom_rocks: # For every rock in both lists, move at speed of 2
            rock.move(2)
   
        # Draw top rocks
        for rock in top_rocks + bottom_rocks: # For every rock in both lists, draw them on the screen
            rock.draw()
    
        # Draw Lives Text 
        lives_text = f"Lives: {lives[0]}"  
        lives_surface = lives_font.render(lives_text, True, (127,0,255)) # Font, and Color (purple)
        lives_rect = lives_surface.get_rect()                            # Gets the position
        lives_rect.topleft = (20,0)                                      # Puts it in the top left corner
        screen.blit(lives_surface, lives_rect)
    
        # Moving plane 
        plane.move(plane_moving_up)

        # Draw the plane
        plane.draw()

    # Check for crash 
    if plane.has_crashed(screen):
        # Game freezes 
        plane_alive = False 
        # Lives go down 
        lives[0] -= 1
        # Wait 
        pygame.time.wait(3000)
        # Plane rests in the middle of the screen
        plane.y = HEIGHT // 2
        plane.draw()
        # Reset background so that the rocks are cleared out 
        top_rocks.clear()
        bottom_rocks.clear()
        # Plane is alive 
        plane_alive = True 

    # Display's Game Over Screen when lives is zero
    if lives[0] == 0:
        display_game_over(screen, WIDTH)
        
        wait_for_restart = True
        while wait_for_restart: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    wait_for_restart = False 
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_RETURN: # If 'enter' is pressed, restart game
                        wait_for_restart = False 
                        lives = [3] # Resets lives 
                        plane_alive = True # Resets plane_alive 
                        plane.y = HEIGHT // 2 # Resets planes position 
                        top_rocks.clear() # Clears top rocks from screen
                        bottom_rocks.clear() # Clears bottom rocks from screen
                    elif event.key == pygame.K_ESCAPE: # if 'esc' is pressed, exits game 
                        running = False 
                        wait_for_restart = False 

    # Flip the display 
    pygame.display.flip()    
    clock.tick(60)  

pygame.quit()