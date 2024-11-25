import pygame 
from datetime import datetime

# Welcome Screen
def display_instructions(screen, WIDTH):
    screen.fill((0,0,0)) # Creates a black screen
    font = pygame.font.Font('Cullen_pygame/Fonts/Kenney_Pixel.ttf', 55)
    spacing = 60

    # Instructions
    instructions = ['Welcome to Flappy Plane', 'Instructions:', 'Press SPACE to move up and down', '', "Press 'Enter' to continue"]

    for i, instruction in enumerate(instructions): # Error gave me 'Cannot unpack non-iterable int'
        text = font.render(instruction, True, (173,216,230)) # Light blue text
        font_rect = text.get_rect()
        font_rect.center = (WIDTH // 2, spacing + i * spacing)
        screen.blit(text, font_rect)
        pygame.display.flip() 

# Game Over Screen 
def display_game_over(bg_music, screen, WIDTH): 
    bg_music.stop() # Stops background music
    screen.fill((0,0,0))
    font = pygame.font.Font('Cullen_pygame/Fonts/Kenney_Pixel.ttf', 55)
    spacing = 60 

    gameover_text = ['GAME OVER', '', "Press 'Enter' to restart"]
    
    for t, gameover in enumerate(gameover_text): # Error gave me 'Cannot unpack non-interable int'
        text = font.render(gameover, True, (255,255,255))
        font_rect = text.get_rect()
        font_rect.center = (WIDTH // 2, spacing + t * spacing)
        screen.blit(text, font_rect)
        pygame.display.flip()

# Taking Screenshots
def take_screenshot(screen):
    fn = datetime.now().strftime('%d_%m_%y_%H%M%S.png')
    # take a screenshot 
    pygame.image.save(screen, f'Cullen_pygame/screenshots/{fn}')