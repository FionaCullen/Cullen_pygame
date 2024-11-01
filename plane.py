from math import cos, sin, pi
import pygame

class Plane():
    def __init__(self, x, y, theta=270, color='red'):
        self.x = x
        self.y = y
        self.speed = 0
        self.theta = theta # degrees
        self.image = pygame.image.load('PNG\Plane\planeRed2.png')

    def deg_to_rad(self, deg):
        # converts deg to rad
        rad = (deg/180) * pi
        return rad

    def update(self):
        # moves our ship at each frame
        # get x and y components of speed
        theta_rad = self.deg_to_rad(self.theta)
        x_dot = cos(theta_rad) * self.speed
        y_dot = sin(theta_rad) * self.speed

        self.x += x_dot
        self.y -= y_dot

    
    def draw(self, screen):
        # rotate our image
        new_image = pygame.transform.rotozoom(self.image, self.theta, 1)
        screen.blit(new_image, (self.x,self.y))