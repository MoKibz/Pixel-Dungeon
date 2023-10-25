import pygame
import pyodbc
from Login_System import NewuserLogin, LoginScreen
from CONSTANTS import Font



# connection with the sql database for
conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)
cursor = conn.cursor()

# initialise the game
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((900, 600))

# Initialize game states
login_screen = LoginScreen()
new_user_login = NewuserLogin(365, 285, 165, 50)

# Initial state
current_state = "menu"  # Start with the login screen

# Create a variable to keep track of button visibility
button_visible = True

# Main game loop
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
                    print('existing user')

    screen.fill((0, 0, 0))  # Black background

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
        # Optionally hide the buttons by setting button_visible to False
        button_visible = False

    pygame.display.update()
    clock.tick(60)