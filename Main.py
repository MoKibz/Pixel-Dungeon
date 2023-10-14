import pygame

# initialise the game
pygame.init()

# set values for the window size
screen = pygame.display.set_mode((900,600))

# set the caption of the window
pygame.display.set_caption("Pixel Dungeon: a roguelike game")

# create a subroutine for the login system
def LoginSystem():
     LoginPage()

def main_menu():
    background_image = pygame.image.load("Images/Wall.png").convert_alpha()
    screen.blit(background_image,(0,0))

def LoginPage():

    # creates the background of the login screen
    background_image = pygame.image.load("Images/Wall.png").convert_alpha()
    screen.blit(background_image, (0, 0))
    # create the new user button
    newuser_button_rect = pygame.Rect(365, 205, 165, 90)
    pygame.draw.rect(screen, "GREY", newuser_button_rect, width=0)
    newuser_Text_x = 385
    newuser_Text_y = 225
    newuser_button_textfont = pygame.font.Font("Font/Handjet-Regular.ttf", 42)
    newuser_button_text = "New User"
    newuser_textsurface = newuser_button_textfont.render(newuser_button_text, True, (255, 255, 255))
    screen.blit(newuser_textsurface, (newuser_Text_x, newuser_Text_y))
    # create the existing user button
    extuser_button_rect = pygame.Rect(365, 305, 165, 90)
    pygame.draw.rect(screen, "GREY", extuser_button_rect, width=0)
    extuser_Text_x = 370
    extuser_Text_y = 325
    extuser_button_textfont = pygame.font.Font("Font/Handjet-Regular.ttf", 36)
    extuser_button_text = "Existing User"
    extuser_textsurface = extuser_button_textfont.render(extuser_button_text, True, (255, 255, 255))
    screen.blit(extuser_textsurface, (extuser_Text_x, extuser_Text_y))


def main():

    # setting a loop that allows the game to be running unless the window is closed
    running = True
    while running:

        LoginSystem()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # checks if the button is clicked
                print("button clicked")

        #main_menu()
        pygame.display.update()

main()


