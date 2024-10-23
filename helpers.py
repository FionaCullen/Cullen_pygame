import pygame

def build_background(WIDTH, HEIGHT):
    # BUILD THE BACKGROUND WITH TILES
    background = pygame.Surface((WIDTH,HEIGHT))
    background.fill((255,0,0))

    # load tile images to variables
    sky = pygame.image.load('PNG/background.png')     
    grass = pygame.image.load('PNG/groundGrass.png')

    # get to the tile_size
    TILE_SIZE = sky.get_width()

    background.blit(sky, (0,0))
    grass_y = HEIGHT-grass.get_height()
    background.blit(grass, (0,grass_y))