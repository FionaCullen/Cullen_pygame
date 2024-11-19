import pygame

class Plane: 
    def __init__(self, HEIGHT, WIDTH, screen): 
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.speed = 3
        self.moving_up = False
        self.plane_height = 36
        self.image = pygame.image.load('Cullen_pygame/PNG/Planes/planeRed2.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 2, self.image.get_height() // 2)) # scaled image to 50 Percent
        # Had to initialize these because they were showing as not defined
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.screen = screen
        self.rect = self.image.get_rect()

    def move(self, move_up):
        self.moving_up = move_up 
        if self.moving_up:        # Only moving is space bar is pressed 
            self.y -= self.speed  # TRUE space bar was pressed, plane moves up 
        else: 
            self.y += self.speed  # FALSE space bar was not pressed, plane false to bottom of screen

        # Bounds for the plane
        if self.y < 0:            # Does not go above the screen
            self.y = 0            # If it does, it gets stuck at 0 (top of the screen)
        elif self.y + self.plane_height > self.HEIGHT:  # Checks to see if bottom of plane has left bottom of screen
            self.y = self.HEIGHT - self.plane_height    # Sets the y position, so it stops before leaving the screen

        self.rect = self.image.get_rect(center = (self.x, self.y))

    # Draws plane
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    def has_crashed(self):
        position = self.rect.midright
        r,g,b,_= self.screen.get_at((position[0] + 1, position[1])) # Setting where the pixel colors are 
        
        print(r,g,b)
        if r in range(230,240) and g in range(240,250) and b in range(245,255): 
           return True 
        return False




