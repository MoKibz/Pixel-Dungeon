import pygame
import pyodbc
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



import pygame
import pyodbc
from CONSTANTS import screen, background_image,Font

conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)

table_name = 'LoginDetails'
column_name = 'Username'
cursor = conn.cursor()

# create a subroutine for the login screen
class LoginScreen:

    def __init__(self):
        # sets the screen background
        screen.blit(background_image, (0, 0))

        # Create the new user button rectangle
        self.NewUsrBtn = pygame.Rect(365, 225, 165, 50)

        # Create the existing user button rectangle
        self.ExtUsrBtn = pygame.Rect(365, 325, 165, 50)

        # Draw the buttons
        pygame.draw.rect(screen, "GREY", self.NewUsrBtn, width=0)
        pygame.draw.rect(screen, "GREY", self.ExtUsrBtn, width=0)

        # Draw the button text
        font = pygame.font.Font(Font, 42)
        newuser_textsurface = font.render("New User", True, (255, 255, 255))
        screen.blit(newuser_textsurface, (385, 225))

        font = pygame.font.Font(Font, 36)
        extuser_textsurface = font.render("Existing User", True, (255, 255, 255))
        screen.blit(extuser_textsurface, (370, 325))

# class used to create the ui for new user and handles the user input when signing in
class NewuserLogin:
    def __init__(self, x, y, width, height):

        self.Font = pygame.font.Font(Font, 30)
        self.Rect = pygame.Rect(x, y, width, height)
        self.entry_complete = False
        # sets the colour
        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour_usr = self.Inactive_Colour
        self.Colour_pwd = self.Inactive_Colour
        self.InputText = ""
        self.Done = False
        self.Active = False
        self.PasswordRect = pygame.Rect(x, y + 60, width, height)
        self.PasswordInputText = ""
        self.PasswordDone = False
        self.PasswordActive = False

    def Draw(self): # displays the objects on the screen
        Input_txt_surface = self.Font.render(self.InputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour_usr, self.Rect)
        screen.blit(Input_txt_surface, (370, 290))

        Input_pwd_txt_surface = self.Font.render(self.PasswordInputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour_pwd, self.PasswordRect)
        screen.blit(Input_pwd_txt_surface, (370, 350))

        Text_usr = self.Font.render("USERNAME:", True, 'BLACK')
        screen.blit(Text_usr, (250,290))

        Text_pwd = self.Font.render("PASSWORD:", True, 'BLACK')
        screen.blit(Text_pwd, (250, 350))

    def GetUsername(self):
        return self.InputText

    def GetDone(self):
        return self.Done

    def Update(self):

        if self.entry_complete:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rect.collidepoint(event.pos):
                    self.Active = True
                else:
                    self.Active = False
                if self.PasswordRect.collidepoint(event.pos):
                    self.PasswordActive = True
                else:
                    self.PasswordActive = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.Active:
                        self.InputText = self.InputText[:-1]
                    elif self.PasswordActive:
                        self.PasswordInputText = self.PasswordInputText[:-1]

                elif event.key == pygame.K_RETURN:
                    if not self.Done:
                        # Check if the username already exists
                        cursor = conn.cursor()
                        query = "SELECT COUNT(*) FROM LoginDetails WHERE Username = ?"
                        cursor.execute(query, self.InputText)
                        result = cursor.fetchone()
                        cursor.close()

                        if result[0] == 0:
                            # If username doesn't exist, insert into the database
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO LoginDetails (Username, User_level) VALUES (?, ?)",
                                           (self.InputText, 1))
                            print(cursor.rowcount, "record inserted")
                            cursor.close()
                            self.Done = True

                        else:
                            print("Username already exists. Choose a different username.")
                    elif not self.PasswordDone and self.Done:
                        # Insert password into the database
                        cursor = conn.cursor()
                        cursor.execute("UPDATE LoginDetails SET Password = ? WHERE Username = ?",
                                       self.PasswordInputText, self.InputText)
                        print(cursor.rowcount, "record updated")
                        cursor.close()
                        self.PasswordDone = True
                        return

                else:
                    # checks the characters being inputted and adding them into the text
                    if self.Active:
                        self.InputText += event.unicode
                    elif self.PasswordActive:
                        self.PasswordInputText += event.unicode

        if self.Active:
            self.Colour_usr = self.Active_Colour
        else:
            self.Colour_usr = self.Inactive_Colour
        if self.PasswordActive:
            self.Colour_pwd = self.Active_Colour
        else:
            self.Colour_pwd = self.Inactive_Colour

# class used to create the ui for existing user login
class ExistingUserLogin:
    def __init__(self, x, y, width, height):

        self.Font = pygame.font.Font(Font, 30)
        self.Rect = pygame.Rect(x, y, width, height)
        self.entry_complete = False
        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour_usr = self.Inactive_Colour
        self.Colour_pwd = self.Inactive_Colour
        self.InputText = ""
        self.Done = False
        self.Active = False
        self.PasswordRect = pygame.Rect(x, y + 60, width, height)
        self.PasswordInputText = ""
        self.PasswordDone = False
        self.PasswordActive = False

    def Draw(self):
        # displays the objects/buttons on the screen
        Input_txt_surface = self.Font.render(self.InputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour_usr, self.Rect)
        screen.blit(Input_txt_surface, (370, 290))

        Input_pwd_txt_surface = self.Font.render(self.PasswordInputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour_pwd, self.PasswordRect)
        screen.blit(Input_pwd_txt_surface, (370, 350))

        Text_usr = self.Font.render("USERNAME:", True, 'BLACK')
        screen.blit(Text_usr, (250, 290))

        Text_pwd = self.Font.render("PASSWORD:", True, 'BLACK')
        screen.blit(Text_pwd, (250, 350))

    def GetUsername(self):
        return self.InputText

    def GetDone(self):
        return self.Done

    def Update(self):

        if self.entry_complete:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rect.collidepoint(event.pos):
                    self.Active = True
                else:
                    self.Active = False
                if self.PasswordRect.collidepoint(event.pos):
                    self.PasswordActive = True
                else:
                    self.PasswordActive = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.Active:
                        self.InputText = self.InputText[:-1]
                    elif self.PasswordActive:
                        self.PasswordInputText = self.PasswordInputText[:-1]
                elif event.key == pygame.K_RETURN:
                    if not self.Done:
                        # Check if the username exists
                        cursor = conn.cursor()
                        query = "SELECT COUNT(*) FROM LoginDetails WHERE Username = ?"
                        cursor.execute(query, self.InputText)
                        result = cursor.fetchone()
                        cursor.close()

                        if result[0] == 1:
                            self.Done = True
                            return
                        else:
                            print("Username does not exist. Enter a valid username.")
                    elif not self.PasswordDone:
                        # Check if the entered password matches the stored password
                        cursor = conn.cursor()
                        query = "SELECT COUNT(*) FROM LoginDetails WHERE Username = ? AND Password = ?"
                        cursor.execute(query, self.InputText, self.PasswordInputText)
                        result = cursor.fetchone()
                        cursor.close()

                        if result[0] == 1:
                            self.PasswordDone = True
                            self.entry_complete = True
                            return
                        else:
                            print("Incorrect password. Enter the correct password.")

                else:
                    if self.Active:
                        self.InputText += event.unicode
                    elif self.PasswordActive:
                        self.PasswordInputText += event.unicode

        if self.Active:
            self.Colour_usr = self.Active_Colour
        else:
            self.Colour_usr = self.Inactive_Colour
        if self.PasswordActive:
            self.Colour_pwd = self.Active_Colour
        else:
            self.Colour_pwd = self.Inactive_Colour



class GameMenu: # class that is used to create the ui after the player has signed up or logged in
    def __init__(self, x, y, width, height):

        self.Font = pygame.font.Font(Font, 40)
        self.Rect = pygame.Rect(x, y, width, height)
        self.Text = "PLAY"
        self.Rect_leaderboard = pygame.Rect(x, y + 60, width + 20, height)
        self.Text_leaderboard = "LEADERBOARD"
        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour = self.Inactive_Colour
        self.Active = False
        self.pressed = False

    def draw(self):
        screen.blit(background_image, (0, 0))
        txt_play = self.Font.render(self.Text, True,'WHITE')
        pygame.draw.rect(screen, self.Colour, self.Rect)
        screen.blit(txt_play, (420, 305))
        txt_leaderboard = self.Font.render(self.Text_leaderboard, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour, self.Rect_leaderboard)
        screen.blit(txt_leaderboard, (410, 365))

    def Update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rect.collidepoint(event.pos):
                    self.Active = True
                    self.pressed = True
                elif self.Rect_leaderboard.collidepoint(event.pos):
                    self.pressed = "YES"
                    print("Leaderboard button pressed ", self.pressed)

                else:
                    self.Active = False

        if self.Active == True:
            self.Colour = self.Active_Colour
        else:
            self.Colour = self.Inactive_Colour

    def Get_pressed(self):
        if self.pressed == True:
            return "PLAY"
        elif self.pressed == "YES":
            return "LEADERBOARD"
        else:
            return False


class LeaderboardMenu(): # class that is used to display the leaderboard
    def __init__(self, player1, player2, player3, player4, player5):
        self.Font = pygame.font.Font(Font, 40)
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.player5 = player5
        self.Rect = pygame.Rect(350, 500, 100, 50)
        self.text = "BACK"
        self.pressed = False

    def draw(self): # draws the leaderboard
        pygame.draw.rect(screen, 'GREY', (300, 100, 200, 300)) # draws the box
        for i in range(5): # draws the leaderboard
            player_name = getattr(self, f"player{i + 1}") # gets the name of the player
            screen.blit(self.Font.render(player_name, True, 'WHITE'), (360, 150 + (i * 50))) # draws the name

        pygame.draw.rect(screen, 'GREEN', self.Rect) # draws the button
        screen.blit(self.Font.render(self.text, True, 'WHITE'), (370, 510)) # draws the text

    def Update(self): # updates the leaderboard
        for event in pygame.event.get(): # checks for events
            if event.type == pygame.QUIT: # exits the game
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # checks if the mouse is clicked
                if self.Rect.collidepoint(event.pos): # checks if the mouse is colliding with the button
                    self.pressed = True

    def Get_pressed(self): # returns the state of the button
        return self.pressed

def get_level(): # gets the user level from the database

    cursor = conn.cursor()
    cursor.execute("SELECT User_level FROM LoginDetails WHERE Username = ?", (Username,))
    Level = cursor.fetchval()
    cursor.close()
    return Level

# Instantiate states of the classes
login_screen = LoginScreen()
new_user_login = NewuserLogin(365, 285, 165, 50)
ext_user_login = ExistingUserLogin(365, 285, 165, 50)
game_menu_inst = GameMenu(400, 300, 100, 50)

def DisplayLeaderboard(): # displays the leaderboard

    cursor = conn.cursor()
    cursor.execute("SELECT Username FROM LoginDetails ORDER BY User_level DESC")
    Usernames = cursor.fetchall()
    cursor.close()

    username_list = [] # empty list to store the usernames
    for row in Usernames: # Iterate over each row in the results set
        # Extract the username from the current row and append it to the username list
        username = row[0]  # the username from the current row is extracted
        username_list.append(username)  # the username is appended to the username list

    leaderboard = LeaderboardMenu(username_list[0], username_list[1], username_list[2], username_list[3], username_list[4]) # instantiates the leaderboardmenu class
    leaderboard.draw() # draws the leaderboard
    leaderboard.Update() # updates the leaderboard
    return leaderboard.Get_pressed() # returns if the back button has been pressed

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
            # update the game menu
            game_menu_inst.Update()
            # stores the value of pressed
            pressed = game_menu_inst.Get_pressed()
            print(pressed)
            if pressed == "PLAY": # if the user presses the play button
                current_state = 'game_started' # switches the state
            elif pressed == "LEADERBOARD": # if the user presses the leaderboard button
                current_state = 'LeaderboardMenu' # switches the state

        elif current_state == "LeaderboardMenu":
            pressed = DisplayLeaderboard() # displays the leaderboard
            if pressed:
                current_state = "game_menu" # switches the state

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

