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

    background_image = pygame.image.load("Images/Wall.png").convert_alpha()
    screen.blit(background_image, (0, 0))
    Button_rect = (345, 212, 200, 75)
    pygame.draw.rect(screen, "GREY", Button_rect, width=0)
    newuser_Text_x = 385
    newuser_Text_y = 225
    newuser_button_textfont = pygame.font.Font("Font/Handjet-Regular.ttf", 42)
    newuser_button_text = "New User"
    newuser_textsurface = newuser_button_textfont.render(newuser_button_text, True, (255, 255, 255))
    screen.blit(newuser_textsurface, (newuser_Text_x, newuser_Text_y))



def main():

    # setting a loop that allows the game to be running unless the window is closed
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        LoginSystem()
        #main_menu()
        pygame.display.update()




main()
