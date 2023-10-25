import pygame

# set the display size
screen = pygame.display.set_mode((900, 600))
# set the caption of the window
pygame.display.set_caption("Pixel Dungeon: a roguelike game")
# set the login page background
background_image = pygame.image.load("Images/Wall.png").convert_alpha()
Font = "Font/Handjet-Regular.ttf"
