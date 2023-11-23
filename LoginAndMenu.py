import pygame
import pyodbc
from CONSTANTS import screen, background_image, Font

conn = pyodbc.connect("driver={SQL Server};"
                      "server=MoKibz\SQLEXPRESS; "
                      "database=UserLoginDetails; "
                      "trusted_connection=true",
                      autocommit=True)

table_name = 'LoginDetails'
column_name = 'Username'
cursor = conn.cursor()




# create a subroutine for the login system
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


class NewuserLogin:
    def __init__(self, x, y, width, height):
        cursor = conn.cursor()
        Table_exists = cursor.execute(
            f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        cursor.close()
        if Table_exists == 0:  # if it does not exist then create the table
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE LoginDetails (
                    Username VARCHAR(255)
                )
                """)
            cursor.close()

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
                    while self.Done == False:
                        cursor = conn.cursor()
                        query = f"SELECT COUNT(*) FROM LoginDetails WHERE Username = ?"
                        cursor.execute(query, self.InputText)
                        result = cursor.fetchone()
                        cursor.close()
                        if result:
                            self.Done = True
                        else:
                            cursor = conn.cursor()
                            cursor.execute(f"INSERT INTO LoginDetails (Username) VALUES (?)",self.InputText)
                            print(cursor.rowcount, "record inserted")
                            cursor.close()
                            self.Done = False

                            break

                    # cursor = conn.cursor()
                    # cursor.execute(f"insert into {table_name} (Username) VALUES ('{self.InputText}')")
                    # cursor.close()
                    # self.Done = not self.Done
                    # self.entry_complete = True


                else:
                    self.InputText += event.unicode



        if self.Active == True:
            self.Colour = self.Active_Colour
        else:
            self.Colour = self.Inactive_Colour


class ExistingUserLogin:
    def __init__(self, x, y, width, height):

        # check if the table exists in the database
        cursor = conn.cursor()
        Table_exists = cursor.execute(
            f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        cursor.close()
        if Table_exists == 0:  # if it does not exist then create the table
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE {table_name}({column_name} varchar(20))")
            cursor.close()

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.InputText = self.InputText[:-1]
                elif event.key == pygame.K_RETURN:
                    cursor = conn.cursor()
                    query = f"SELECT COUNT(*) FROM LoginDetails WHERE Username = ?"
                    cursor.execute(query, self.InputText)
                    result = cursor.fetchone()
                    cursor.close()
                    if result[0] == 1:
                        self.Done = False
                        break
                    else:
                        self.Done = True
                        self.entry_complete = True
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
