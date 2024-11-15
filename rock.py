import pygame 
import random

class Rock: 
    def __init__(self, top_rock, max_height):
        self.top_rock = top_rock
        self.max_height = max_height
        self.rock_x = WIDTH + random.randint(0,200)
        self.rock_width = random.randint(50,150)
        self.rock_height = random.randint(100, max_height)

        if self.top_rock:  # If top rock the y position is zero (top of screen)
            self.rock_y = 0 
        else:              # If not top rock, it has to be bettom rock- y position at bottom of screen
            self.rock_y = HEIGHT - self.rock_height

        if self.top_rock:  # If top rock print the upside rock image 
            self.image = pygame.image.load('Cullen_pygame/PNG/rockGrassDown.png')
        else:              # If not top rock, print bottom rock image
            self.image = pygame.image.load('Cullen_pygame/PNG/rockGrass.png')

        
    def move(self, speed):  # Moves left on the screen, at the same speed as the screen
        self.rock_x -= speed 

    def offscreen(self): # Checks to see if the right most edge of the image has left the screen 
        return self.rock_x + self.rock_width < 0 
    
    def draw(self): # Draw the rock at its location
        screen.blit(self.image, (self.rock_x, self.rock_y))