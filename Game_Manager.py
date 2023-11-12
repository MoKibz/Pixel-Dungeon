import pygame, sys
import pyodbc
from LoginAndMenu import LoginScreen, NewuserLogin, ExistingUserLogin, GameMenu
from CONSTANTS import *
import random




# connection with the sql database for
conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)

cursor = conn.cursor()

Table_exists = cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'LoginDetails'")

# if Table_exists == 0:
#     cursor.execute("CREATE TABLE LoginDetails ("
#                    "Username VARCHAR()")


# initialize the game
pygame.init()
clock = pygame.time.Clock()
# set the display size
screen = pygame.display.set_mode((900, 600))
# set the font
Game_Font = pygame.font.Font(Font, 50)


class Game_map:
    def __init__(self):
        self.Map_1 = tilemap
        self.tile_size = 30
        self.tile_key = {'G': Ground_tile,
                    'W': Wall_tile_resized,
                    'W_R': Wall_tile_r_resized,
                    'W_L': Wall_tile_l_resized,
                    'W_B': Wall_tile_Bottom_resized,
                    'W_BRC': Wall_tile_BRC_resized,
                    'W_BLC': Wall_tile_BLC_resized
                    }

    def Draw_map(self):
        screen.fill("BLACK")
        for y, row in enumerate(self.Map_1):
            for x, tile_type in enumerate(row):
                tile_image = self.tile_key.get(tile_type)
                if tile_image:
                    screen.blit(tile_image,(x * self.tile_size, y * self.tile_size))

        # Get_Character()

def Get_Character(Character):
    CharacterType = ["shooter", "melee"]

    class Characters(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self._Alive = True
            self.level = 1
            self.movement_speed = 10
            self.Type = ['close_range', 'long_range']
            self.attack_range = {self.Type[0]: 30,
                                 self.Type[1]: 210}
            self.defence = 100
            self.health = 100
            self.Weapons = ['gun', 'sword']
            self.Potions = ['health_potion', 'defence_potion']


        def is_alive(self):
            if self._Alive == False:
                print("My boi died")




    class Shooter(Characters):
        def __init__(self):
            super().__init__()
            self.lvl = self.level
            self.Character_Type = self.attack_range[self.Type[1]]
            self.Stats = [self.health, (self.defence - 20)]
            self.speed = self.movement_speed - 2
            self.Shooter_item = [self.Weapons[1], ]

        def Draw(self):
            pass

    class Melee(Characters):
        def __init__(self):
            super().__init__()
            self.lvl = self.level
            self.Character_Type = self.attack_range[self.Type[0]]
            self.Stats = [self.health, (self.defence + 10)]
            self.speed = self.movement_speed + 5

        def Draw(self):
            self.image = Melee_char_resized
            self.Char_rect = self.image.get_rect()
            self.Char_rect = [2 * 30, 3 * 30]

    class Enemies(Characters):
        def __init__(self):
            super().__init__()




    if Character == CharacterType[0]:
        Character = Shooter()
        Character.Draw()
    elif Character == CharacterType[1]:
        Character = Melee()
        Character.Draw()




# def Game_control():
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()





def Game():
    GameMapInst = Game_map()
    Melee_option_rect = pygame.rect.Rect(400, 200, 200, 70)
    Melee_option_rect.center = [450, 200]
    Melee_option_text = Game_Font.render("MELEE", True, 'WHITE')
    Melee_option_text_rect = Melee_option_text.get_rect(center=Melee_option_rect.center)
    Shooter_option_rect = pygame.rect.Rect(400, 200, 200, 70)
    Shooter_option_rect.center = [450, 400]
    Shooter_option_text = Game_Font.render("SHOOTER", True, 'WHITE')
    Shooter_option_text_rect = Shooter_option_text.get_rect(center=Shooter_option_rect.center)
    Character = ""
    GameState = "character_selection"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Melee_option_rect.collidepoint(event.pos):
                    Character = "melee"
                    Get_Character(Character)
                if Shooter_option_rect.collidepoint(event.pos):
                    Character = "shooter"
                    Get_Character(Character)



        if GameState == "character_selection":
            pygame.draw.rect(screen, "GREY", Melee_option_rect)
            screen.blit(Melee_option_text, Melee_option_text_rect)
            pygame.draw.rect(screen, "GREY", Shooter_option_rect)
            screen.blit(Shooter_option_text, Shooter_option_text_rect)





        pygame.display.update()
        clock.tick(60)


# Initialize game states
login_screen = LoginScreen()
new_user_login = NewuserLogin(365, 285, 165, 50)
ext_user_login = ExistingUserLogin(365, 285, 165, 50)
game_menu_inst = GameMenu(400, 300, 100, 50)
# loop
def Initial_system_manager():
    # Initial state
    current_state = "menu"  # Start with the login screen
    # Create a variable to keep track of button visibility
    button_visible = True
    Username_printed = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_visible and login_screen.NewUsrBtn.collidepoint(event.pos):
                        # Transition to the "New User" state
                        current_state = "new_user"
                    elif button_visible and login_screen.ExtUsrBtn.collidepoint(event.pos):
                        current_state = "ext_user"


        screen.blit(background_image, (0, 0))

        if current_state == "menu":
            # Draw the buttons directly in the main module
            pygame.draw.rect(screen, "GREY", login_screen.NewUsrBtn, width=0)
            pygame.draw.rect(screen, "GREY", login_screen.ExtUsrBtn, width=0)

            font = pygame.font.Font(Font, 42)
            newuser_textsurface = font.render("New User", True, (255, 255, 255))
            screen.blit(newuser_textsurface, (385, 225))

            font = pygame.font.Font(Font, 36)
            extuser_textsurface = font.render("Existing User", True, (255, 255, 255))
            screen.blit(extuser_textsurface, (370, 325))

        elif current_state == "new_user":
            # Draw the "New User" input boxes

            new_user_login.Draw()

            new_user_login.Update()

            Username, Done = new_user_login.GetUsername()

            if Done and not Username_printed:
                print(Username)
                # cursor.execute('')
                current_state = "game_menu"
                Username_printed = True

            button_visible = False
        elif current_state == "ext_user":
            ext_user_login.Draw()

            ext_user_login.Update()

            Username, Done = ext_user_login.GetUsername()

            if Done and not Username_printed:

                # cursor.execute('')
                current_state = "game_menu"
                Username_printed = True

            button_visible = False
        elif current_state == "game_menu":
            game_menu_inst.draw()

            game_menu_inst.Update()

            pressed = game_menu_inst.Get_pressed()

            if pressed:
                current_state = 'game_started'

        elif current_state == "game_started":

            break



        pygame.display.update()
        clock.tick(1000)



if __name__ == "__main__":
    Initial_system_manager()
    Game()
