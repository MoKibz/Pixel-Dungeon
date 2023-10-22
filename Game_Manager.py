import pygame
import pyodbc
import Login_System

# connection with the sql database for
conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)
cursor = conn.cursor()

# initialise the game
pygame.init()

# set values for the window size
screen = pygame.display.set_mode((900, 600))

# set the caption of the window
pygame.display.set_caption("Pixel Dungeon: a roguelike game")

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # checks if the button is clicked

            print("Clicked")

    Login_System.LoginSys(screen)

    # main_menu()
    pygame.display.update()

