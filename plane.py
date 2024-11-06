from math import cos, sin, pi
import pygame

plane = pygame.image.load('Cullen_pygame/PNG/plane.png')
plane_width = plane.get_width()
plane_height = plane.get_height()

plane_x = WIDTH // 4
plane_y = HEIGHT // 2
plane_speed = 5 

keys = pygame.key.get_pressed()
if keys[pygame.K_SPACE]:
    plane_y -= plane_speed
else: 
    plane_y += plane_speed 

plane_y = max(0, min(HEIGHT - plane_height, plane_y))

screen.blit(plane, (plane_x, plane_y))
