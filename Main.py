import pygame, sys
import pyodbc
from LoginAndMenu import LoginScreen, NewuserLogin, ExistingUserLogin, GameMenu
from CONSTANTS import *
import random


# initialize the game
pygame.init()
clock = pygame.time.Clock()
# set the display size
screen = pygame.display.set_mode((900, 600))
# set the font
Level = 1
# class used to draw the game maps
class Game_map:

    def __init__(self):
        self.tilemap = None
        if Level == 1:
            self.tilemap = tilemap1
        elif Level == 2:
            self.tilemap = tilemap2
        self.Map_1 = self.tilemap
        self.tile_size = 30
        self.tile_key = {'G': Ground_tile,
                        'W': Wall_tile_resized,
                        'W_R': Wall_tile_r_resized,
                        'W_L': Wall_tile_l_resized,
                        'W_B': Wall_tile_Bottom_resized,
                        'W_BRC': Wall_tile_BRC_resized,
                        'W_BLC': Wall_tile_BLC_resized,
                        'W_CR1': Wall_Corner1,
                        'W_CR2': Wall_Corner2,
                        'W_CR3': Wall_Corner3,
                        'W_CR4': Wall_Corner4
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
            self._level = Level
            self._movement_speed = 2
            self._Type = ['close_range', 'long_range']
            self.attack_range = {self._Type[0]: 30,
                                 self._Type[1]: 210}
            self.defence = 100
            self.health = 100
            self._Weapons = ['gun', 'sword']
            self._Potions = ['health_potion', 'defence_potion']


        def is_alive(self):
            if self._Alive == False:
                print("My boi died")

    class Shooter(Characters):
        def __init__(self):
            super().__init__()
            self.lvl = self._level
            self.Character_Type = self.attack_range[self._Type[1]]
            self.Stats = [self.health, (self.defence - 20)]
            self.speed = self._movement_speed
            self.Shooter_item = [self._Weapons[1]]
            self.image = Shooter_char_resized
            self.Char_rect = self.image.get_rect()
            self.Char_rect.topleft = (0 * 30, 1 * 30)

        def movement(self, dx, dy):
            self.Char_rect.x += dx
            self.Char_rect.y += dy

        def Draw(self):
            screen.blit(self.image, self.Char_rect)

    class Melee(Characters):
        def __init__(self):
            super().__init__()
            self.Character_Type = self.attack_range[self._Type[0]]
            self.Stats = [self.health, (self.defence + 10)]
            self.speed = self._movement_speed + 5
            self.image = Melee_char_resized
            self.Char_rect = self.image.get_rect()
            self.Char_rect.topleft = (0 * 30, 1 * 30)

        def movement(self, dx, dy):
            self.Char_rect.x += dx
            self.Char_rect.y += dy

        def Draw(self):
            screen.blit(self.image, self.Char_rect)

        def Health_bar(self):
            pass

    class Enemies(Characters):
        def __init__(self):
            super().__init__()


    if Character == CharacterType[0]:
        return Shooter()
    elif Character == CharacterType[1]:
        return Melee()

def Game():
    GameMapInst = Game_map()
    Character = None
    GameState = "character_selection"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if GameState == "character_selection":
                Melee_option_rect = pygame.rect.Rect(400, 200, 200, 70)
                Melee_option_rect.center = [450, 200]
                Melee_option_text = Game_Font.render("MELEE", True, 'WHITE')
                Melee_option_text_rect = Melee_option_text.get_rect(center=Melee_option_rect.center)
                Shooter_option_rect = pygame.rect.Rect(400, 200, 200, 70)
                Shooter_option_rect.center = [450, 400]
                Shooter_option_text = Game_Font.render("SHOOTER", True, 'WHITE')
                Shooter_option_text_rect = Shooter_option_text.get_rect(center=Shooter_option_rect.center)
                pygame.draw.rect(screen, "GREY", Melee_option_rect)
                screen.blit(Melee_option_text, Melee_option_text_rect)
                pygame.draw.rect(screen, "GREY", Shooter_option_rect)
                screen.blit(Shooter_option_text, Shooter_option_text_rect)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Melee_option_rect.collidepoint(event.pos):
                        Character = Get_Character("melee")
                        GameState = "game_started"
                    elif Shooter_option_rect.collidepoint(event.pos):
                        Character = Get_Character("shooter")
                        GameState = "game_started"

            elif GameState == "game_started":

                keys = pygame.key.get_pressed()  # Get the state of all keys

                # Copy the character's current position before attempting to move
                prev_position = Character.Char_rect.topleft

                dx = 0
                dy = 0

                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    dx = -Character.speed
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    dx = Character.speed
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    dy = -Character.speed
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    dy = Character.speed

                # Update the character's position
                Character.movement(dx, dy)

                # Check for collisions with wall tiles
                for y, row in enumerate(GameMapInst.Map_1):
                    for x, tile_type in enumerate(row):
                        if tile_type.startswith('W') and Character.Char_rect.colliderect(x * GameMapInst.tile_size,
                                                                                         y * GameMapInst.tile_size,
                                                                                         GameMapInst.tile_size,
                                                                                         GameMapInst.tile_size):
                            # Collision detected with a wall tile, revert the character's position
                            Character.Char_rect.topleft = prev_position

                GameMapInst.Draw_map()
                Character.Draw()

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

            if Done:
                print(Username)
                # cursor.execute('')
                current_state = "game_menu"


            button_visible = False
        elif current_state == "ext_user":
            ext_user_login.Draw()

            ext_user_login.Update()

            Done = ext_user_login.GetUsername()

            if Done:

                # cursor.execute('')
                current_state = "game_menu"


            button_visible = False
        elif current_state == "game_menu":
            # draw the game menu using the instance of the class
            game_menu_inst.draw()
            # checks if the user is pressed the start button
            game_menu_inst.Update()
            # stores the value of pressed
            pressed = game_menu_inst.Get_pressed()
            if pressed: # checks if pressed = true
                current_state = 'game_started'

        elif current_state == "game_started":

            break

        pygame.display.update()
        clock.tick(1000)
    if current_state == "game_started":
        return True

if __name__ == "__main__":
    Started = Initial_system_manager()
    if Started:
        Game()
