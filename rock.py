import pygame 
import random

class Rock: 
    def __init__(self, top_rock, screen, WIDTH, HEIGHT):
        self.top_rock = top_rock
        # Had to add these because they were showing as not defined 
        self.WIDTH = WIDTH 
        self.HEIGHT = HEIGHT 
        self.screen = screen

        self.rock_height = random.randint(100, 237)
        self.rock_width = random.randint(50,150)
        self.rock_x = WIDTH + random.randint(0,200) # Makes rocks appear to slide onto the screen
     

        if self.top_rock: 
            self.rock_y = 0 - (260 - self.rock_height)  # Makes bottom of the rock flush with the top of the screen
        else:              
            self.rock_y = self.HEIGHT - self.rock_height # If not top rock, it is bottom rock- y position at bottom of screen

        if self.top_rock:  
            self.image = pygame.image.load('Cullen_pygame/PNG/rockGrassDown.png')
        else:             
            self.image = pygame.image.load('Cullen_pygame/PNG/rockGrass.png')

    # Move 
    def move(self, speed):  # Moves left on the screen, at the same speed as the screen
        self.rock_x -= speed 

    # Check to see if rocks are off screen
    def offscreen(self): # Checks to see if the right most edge of the image has left the screen 
        return self.rock_x + self.rock_width < 0 # right most part of the rock is less than zero (left most edge of the screen) = offscreen

    # Draw the rocks onto the screen
    def draw(self): 
        self.screen.blit(self.image, (self.rock_x, self.rock_y))