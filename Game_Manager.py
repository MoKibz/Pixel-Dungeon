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

#creates a loop that keeps the game running unless the player exits the game or closes the game window
running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT: # checks if the user closes the window
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # checks if the user presses the mouse
            if event.button == 1:  # checks left mouse button clicked
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if NewUsrBtn.collidepoint(mouse_x, mouse_y): # checks if the NewUsrBtn is clicked
                    print("New user!")
                elif ExtUsrBtn.collidepoint(mouse_x, mouse_y): # checks if the ExtUsrBtn is clicked
                    print("Existing user!")

    NewUsrBtn, ExtUsrBtn = Login_System.LoginScreen(screen)

    # refreshes the window
    pygame.display.update()

