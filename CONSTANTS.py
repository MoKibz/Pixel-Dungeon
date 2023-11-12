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
Wall_tile_resized = pygame.transform.scale(Wall_tile, (30, 30))
Wall_tile_r = pygame.image.load("Images/Dungeon_Tileset_SIDES_R.png")
Wall_tile_r_resized = pygame.transform.scale(Wall_tile_r, (30, 30))
Wall_tile_l = pygame.image.load("Images/Dungeon_Tileset_SIDES_L.png")
Wall_tile_l_resized = pygame.transform.scale(Wall_tile_l, (30, 30))
Wall_tile_Bottom = pygame.image.load("Images/Dungeon_Tileset_Wall_bottom.png")
Wall_tile_Bottom_resized = pygame.transform.scale(Wall_tile_Bottom, (30,30))
Wall_tile_BRC = pygame.image.load("Images/Dungeon_Tileset_wall_BRC.png")
Wall_tile_BRC_resized = pygame.transform.scale(Wall_tile_BRC, (30,30))
Wall_tile_BLC = pygame.image.load("Images/Dungeon_Tileset_wall_BLC.png")
Wall_tile_BLC_resized = pygame.transform.scale(Wall_tile_BLC, (30,30))
Melee_char = pygame.image.load("Images/Dungeon_Character_melee.png")
Melee_char_resized = pygame.transform.scale(Melee_char,(30,30))

tilemap = [
    ['W_L','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W_R'],
    ['G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_L','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','G','W_R'],
    ['W_BRC','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_B','W_BLC']
]

