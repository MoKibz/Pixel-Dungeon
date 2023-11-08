import pygame
# import pyodbc
from CONSTANTS import screen, background_image, Font

# conn = pyodbc.connect("driver={SQL Server};"
#                       "server=MoKibz\SQLEXPRESS; "
#                       "database=UserLoginDetails; "
#                       "trusted_connection=true",
#                       autocommit=True)
# cursor = conn.cursor()


# create a subroutine for the login system
class LoginScreen:

    def __init__(self):
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


class NewuserLogin:
    def __init__(self, x, y, width, height):
        self.Font = pygame.font.Font(Font, 30)
        self.Rect = pygame.Rect(x, y, width, height)
        self.entry_complete = False

        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour = self.Inactive_Colour
        self.InputText = ""
        self.Done = False
        self.Active = False



    def Draw(self):
        Input_txt_surface = self.Font.render(self.InputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour, self.Rect)
        screen.blit(Input_txt_surface, (370, 290))

    def GetUsername(self):
        return self.InputText, self.Done

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.InputText = self.InputText[:-1]
                elif event.key == pygame.K_RETURN:
                    self.Done = not self.Done
                    self.entry_complete = True
                    break
                else:
                    self.InputText += event.unicode



        if self.Active == True:
            self.Colour = self.Active_Colour
        else:
            self.Colour = self.Inactive_Colour


class ExistingUserLogin:
    def __init__(self, x, y, width, height):
        self.Font = pygame.font.Font(Font, 30)
        self.Rect = pygame.Rect(x, y, width, height)
        self.entry_complete = False

        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour = self.Inactive_Colour
        self.InputText = ""
        self.Done = False
        self.Active = False



    def Draw(self):
        Input_txt_surface = self.Font.render(self.InputText, True, 'WHITE')
        pygame.draw.rect(screen, self.Colour, self.Rect)
        screen.blit(Input_txt_surface, (370, 290))

    def GetUsername(self):
        return self.InputText, self.Done

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.InputText = self.InputText[:-1]
                elif event.key == pygame.K_RETURN:
                    self.Done = not self.Done
                    self.entry_complete = True
                    break
                else:
                    self.InputText += event.unicode



        if self.Active == True:
            self.Colour = self.Active_Colour
        else:
            self.Colour = self.Inactive_Colour


class GameMenu:

    def __init__(self, x, y, width, height):

        self.Font = pygame.font.Font(Font, 40)
        self.Rect = pygame.Rect(x, y, width, height)
        self.Text = "PLAY"
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

    def Update(self):

        # if self.pressed:
        #     return self.pressed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.Rect.collidepoint(event.pos):
                    self.Active = True
                    self.pressed = True
                else:
                    self.Active = False

        if self.Active == True:
            self.Colour = self.Active_Colour
        else:
            self.Colour = self.Inactive_Colour

    def Get_pressed(self):
        return self.pressed
