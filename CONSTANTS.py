import pygame

# set the display size
screen = pygame.display.set_mode((900, 600))
# set the caption of the window
pygame.display.set_caption("Pixel Dungeon: a roguelike game")
# set the login page background
background_image = pygame.image.load("Images/Wall.png").convert_alpha()
Font = "Font/Handjet-Regular.ttf"
Ground_tile = pygame.image.load("Images/Dungeon_Tileset_ground.png")
Wall_tile = pygame.image.load("Images/Dungeon_Tileset_wall.png")

tilemap = [
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
    '.GGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WGGGGGGGGGGGGGGGGGGGGGGGGGGGGW',
    'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW']

for x in tilemap:
    for i in x:
        print(i)