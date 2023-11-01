import pygame
import pyodbc
from LoginAndMenu import LoginScreen, NewuserLogin, ExistingUserLogin, GameMenu
from CONSTANTS import Font, background_image



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

# Initialize game states
login_screen = LoginScreen()
new_user_login = NewuserLogin(365, 285, 165, 50)
ext_user_login = ExistingUserLogin(365, 285, 165, 50)
game_menu_inst = GameMenu(400, 300, 100, 50)

# Initial state
current_state = "menu" # Start with the login screen

# Create a variable to keep track of button visibility
button_visible = True
Username_printed = False

# def Game():
#
#     GameRunning = True
#     while GameRunning:
#         screen.blit(background_image, (0, 0))
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 GameRunning = False






# loop
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
        elif current_state == "game_started":
            print(current_state)
            pygame.time.delay(5000)
            quit()


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
            print(Username)
            # cursor.execute('')
            current_state = "game_menu"
            Username_printed = True

        button_visible = False
    elif current_state == "game_menu":
        game_menu_inst.draw()

        pressed = game_menu_inst.Update()

        if pressed:
            current_state = 'game_started'







    pygame.display.update()
    clock.tick(1000)
