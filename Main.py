import pygame
import pyodbc
from LoginAndMenu import LoginScreen, NewuserLogin, ExistingUserLogin, GameMenu
from CONSTANTS import *
import random

# create a connection to the database
conn = pyodbc.connect("driver={SQL Server};"
                      "server=MOKIBZ\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)

# initialize the game
pygame.init()
clock = pygame.time.Clock()
# set the display size
screen = pygame.display.set_mode((900, 600))
Username = ""
projectiles = []  # List to store projectiles
# Instantiate states of the classes
login_screen = LoginScreen()
new_user_login = NewuserLogin(365, 285, 165, 50)
ext_user_login = ExistingUserLogin(365, 285, 165, 50)
game_menu_inst = GameMenu(400, 300, 100, 50)


def get_level(): # gets the user level from the database

    cursor = conn.cursor()
    cursor.execute("SELECT User_level FROM LoginDetails WHERE Username = ?", (Username,))
    Level = cursor.fetchval()
    cursor.close()
    return Level

# class used to draw the game maps
class Game_map:

    def __init__(self):
        self.tilemap = None
        self.Level = get_level() # uses the get_level subroutine to acquire the player level from their respective account

        # gets the appropriate map for the user according to their level
        if self.Level == 1:
            self.tilemap = tilemap1
        elif self.Level == 2:
            self.tilemap = tilemap2
        self.Map = self.tilemap
        self.tile_size = 30 # sets the size of each tile
        # uses a dictionary to contain the key for each type of tile
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

    def Draw_map(self): # used to draw the map
        screen.fill("BLACK") # sets the background colour to black
        for y, row in enumerate(self.Map):
            for x, tile_type in enumerate(row):
                tile_image = self.tile_key.get(tile_type)
                if tile_image:
                    screen.blit(tile_image,(x * self.tile_size, y * self.tile_size))

def Get_Character(Character):
    CharacterType = ["shooter", "melee"]

    if Character == CharacterType[0]:
        return Shooter()
    elif Character == CharacterType[1]:
        return Melee()

class Characters():

    def __init__(self):
        super().__init__()
        self._Alive = True
        self._level = 1
        self._movement_speed = 2
        self._Type = ['close_range', 'long_range']
        self.attack_range = {self._Type[0]: 30,
                             self._Type[1]: 210}
        self.defence = 100
        self.health = 100
        self._Weapons = ['gun', 'sword']
        self._Potions = ['health_potion', 'defence_potion']

    def Gethealth(self):
        return self.health

    def is_alive(self, alive):
        self._Alive = alive
        if self._Alive == False:
            screen.fill('BLACK')
            game_over_text = Game_Font.render("Game Over! You Died.", True, (255, 0, 0))
            screen.blit(game_over_text, (300, 250))
            pygame.display.update()
            pygame.time.delay(2000)  # Display message for 2 seconds
            return False


class Shooter(Characters):
    def __init__(self):
        super().__init__()
        global projectiles
        self.lvl = self._level
        self.Character_Type = self.attack_range[self._Type[1]]
        self.Stats = [self.health, (self.defence - 20)]
        self.speed = self._movement_speed + 2
        self.Shooter_item = [self._Weapons[1]]
        self.image = Shooter_char_resized
        self.Char_rect = self.image.get_rect()
        self.Char_rect.topleft = (0 * 30, 1 * 30)

    def movement(self, dx, dy):
        self.Char_rect.x += dx
        self.Char_rect.y += dy

    def Draw(self):
        screen.blit(self.image, self.Char_rect)

    def Shoot(self, Last_x_pos, Last_y_pos):

        new_projectile = Projectile(self.Char_rect.centerx, self.Char_rect.centery, Last_x_pos, Last_y_pos)
        projectiles.append(new_projectile)

    def UpdateProjectile(self):
        for projectile in projectiles:
            projectile.update()

    def GetDefence(self):
        return self.Stats[1]

class Projectile:
    def __init__(self, x, y, target_x, target_y):
        self.x = x  # Initial x position of the projectile
        self.y = y  # Initial y position of the projectile
        self.target_x = target_x  # Target x position (where the projectile is aimed)
        self.target_y = target_y  # Target y position (where the projectile is aimed)
        self.speed = 3  # Speed of the projectile
        self.image = ShootingBall_resized  # Image of the projectile
        self.rect = self.image.get_rect()  # Rect object for collision detection
        self.rect.center = (self.x, self.y)  # Set the center of the rect to the initial position

    def update(self):
        if self.x != self.target_x:
            # Update the position of the projectile based on its speed and direction
            self.x += self.speed  # Move left (decrease x-coordinate)
            self.rect.center = (self.x, self.y)  # Update the rect position accordingly


    def draw(self, screen):
        # Draw the projectile onto the screen
        screen.blit(self.image, self.rect)

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

    def GetDefence(self):
        return self.Stats[1]

class Enemy:
    def __init__(self, position_x, position_y):
        self.Alive = True
        self.image = enemy_resized
        self.Char_rect = self.image.get_rect()
        self.Char_rect.topleft = (position_x * 30, position_y * 30)
        self.health = 50

    def Draw(self):
        screen.blit(self.image, self.Char_rect)



class HealthBar:
    def __init__(self, x, y, width, height, Character):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = Character.Gethealth()
        self.health = self.max_health

    def draw(self, screen):
        font = pygame.font.Font(Font, 12)
        # calculates the width of the health bar based on the current health percentage
        health_ratio = self.health / self.max_health
        bar_width = int(self.width * health_ratio)
        text = font.render("H P", True, 'WHITE')

        # Draws the background of the health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draws the remaining health bar (in green)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, bar_width, self.height))
        screen.blit(text, (752, 51))

    def set_health(self, health):
        self.health = health

class DefenceBar:
    def __init__(self, x, y, width, height, Character):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_Defence = Character.GetDefence()
        self.Defence = self.max_Defence

    def draw(self, screen):
        font = pygame.font.Font(Font, 12)
        # calculates the width of the health bar based on the current health percentage
        health_ratio = int(self.Defence / self.max_Defence)
        bar_width = int(self.width * health_ratio)
        text = font.render("DEF", True, 'WHITE')

        # Draws the background of the health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # Draws the remaining health bar (in green)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, bar_width, self.height))
        screen.blit(text, (752, 71))

    def set_Defence(self, Defence):
        self.Defence = Defence

def Game():
    global projectiles
    Character = None
    health_bar = None
    defence_bar = None
    GameMapInst = Game_map()
    GameState = "character_selection"
    player_health = 100
    running = True
    RandomNum1 = random.randint(2, 15)
    RandomNum2 = random.randint(2, 12)
    RandomNum3 = random.randint(2, 15)
    RandomNum4 = random.randint(2, 12)
    RandomNum5 = random.randint(2, 15)
    RandomNum6 = random.randint(2, 12)

    enemy1 = Enemy(RandomNum1, RandomNum2)
    enemy2 = Enemy(RandomNum3, RandomNum4)
    enemy3 = Enemy(RandomNum5, RandomNum6)

    while running:
        try:
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
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            if isinstance(Character, Shooter):
                                Character.Shoot((Character.Char_rect.centerx + 40), Character.Char_rect.centery)

                    prev_position = Character.Char_rect.centerx

                    for enemy in [enemy1, enemy2, enemy3]:
                        if Character.Char_rect.colliderect(enemy.Char_rect):
                            # Collision detected between player and enemy
                            if player_health > 0:
                                player_health -= 10  # Deduct 10 from player's health
                                print("Player health:", player_health)
                                health_bar.set_health(player_health)  # Update the health bar
                            elif player_health <= 0:
                                running = Character.is_alive(False)

                    if health_bar == None:
                        health_bar = HealthBar(750, 50, 100, 14, Character)
                    if defence_bar == None:
                        defence_bar = DefenceBar(750, 70, 100, 14, Character)

                    keys = pygame.key.get_pressed()  # Get the state of all keys

                    dx = 0
                    dy = 0

                    # Inside the "game_started" state of the while loop
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # move the character to the left
                        dx = -Character.speed

                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # move the character to the right
                        dx = Character.speed

                    if keys[pygame.K_UP] or keys[pygame.K_w]:  # move the character up
                        dy = -Character.speed
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:  # move the character down
                        dy = Character.speed

                    # Update the character's position
                    Character.movement(dx, dy)

                    # Check for collisions with wall tiles
                    for y, row in enumerate(GameMapInst.Map):
                        for x, tile_type in enumerate(row):
                            if tile_type.startswith('W') and Character.Char_rect.colliderect(x * GameMapInst.tile_size,
                                                                                             y * GameMapInst.tile_size,
                                                                                             GameMapInst.tile_size,
                                                                                             GameMapInst.tile_size):
                                # if any collision detected with a wall tile, revert to character's previous position
                                Character.Char_rect.centerx = prev_position

                    player_defence = Character.GetDefence()  # get character defence stat
                    GameMapInst.Draw_map()  # display the map
                    Character.Draw()  # display the character
                    enemy1.Draw()
                    enemy2.Draw()
                    enemy3.Draw()
                    health_bar.set_health(player_health)
                    health_bar.draw(screen)  # draw the health bar
                    defence_bar.set_Defence(player_defence)
                    defence_bar.draw(screen)  # draw the defence bar

            for projectile in projectiles:
                projectile.update()

            # Draws the projectiles
            for projectile in projectiles:
                projectile.draw(screen)

            pygame.display.update()  # updating the screen
            clock.tick(60) # setting the refresh rate at 60 fps

        except Exception as e:
            print("An error occurred while handling pygame events:", e)


def Initial_system_manager():
    global Username
    # Initial state
    current_state = "menu"  # Start with the login screen
    # Create a variable to keep track of button visibility
    button_visible = True
    running = True
    while running:
        try:
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
        except Exception as e:
            print("Error: ", e)

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

            new_user_login.Draw() # used to display the newuser login stage

            new_user_login.Update() # updates the screen

            Username = new_user_login.GetUsername() # gets the username
            Done = new_user_login.GetDone() # checks if this stage is finished

            if Done:
                # switch state
                current_state = "game_menu"

            button_visible = False

        elif current_state == "ext_user":
            ext_user_login.Draw() # used to display the existing user login stage

            ext_user_login.Update()  # used to update the screen

            Username = ext_user_login.GetUsername() # gets the username


            Done = ext_user_login.GetDone() # checks if this stage is finished

            if Done:
                # switch state
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
        clock.tick(10000) # sets the clock tick (refresh rate)
    if current_state == "game_started":
        return True

if __name__ == "__main__": # this if statement is used to ensure the code is executed in the correct order of subroutines
    Started = Initial_system_manager()
    if Started:
        print(Username)
        Game()