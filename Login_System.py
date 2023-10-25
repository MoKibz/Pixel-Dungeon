import pygame
import pyodbc
from CONSTANTS import screen, background_image, Font

conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)
cursor = conn.cursor()


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


class NewuserLogin():
    def __init__(self, x, y, width, height):
        self.Font = pygame.font.Font(Font, 40)
        self.Rect = pygame.Rect(x, y, width, height)
        #self.Rect = pygame.Rect(365, 285, 165, 50)

        self.Active_Colour = pygame.Color('GREEN')
        self.Inactive_Colour = pygame.Color('GREY')
        self.Colour = self.Inactive_Colour
        self.InputText = ""

        self.Active = False



    def Draw(self):
        Input_txt_surface = self.Font.render(self.InputText, True, self.Colour)
        width = max(self.Rect.w, Input_txt_surface.get_width() + 10)
        self.Rect.w = width
        screen.blit(Input_txt_surface, (self.Rect.x + 5, self.Rect.y + 5))
        pygame.draw.rect(screen, self.Colour, self.Rect)

    def Update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.Rect.collidepoint(event.pos):
                self.Active = not self.Active
            else:
                self.Active = False
            self.Colour = self.Active_Colour if self.Active else self.Inactive_Colour
        if event.type == pygame.KEYDOWN:
            if self.Active:
                if event.key == pygame.K_RETURN:
                    self.Active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.InputText = self.InputText[:-1]
                else:
                    self.InputText += event.unicode

    def is_active(self):
        return self.Active

    def get_text(self):
        return self.InputText

    def clear_text(self):
        self.text = ''

