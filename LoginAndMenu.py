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
        return self.InputText, self.Done

    def GetPassword(self):
        return self.PasswordInputText, self.PasswordDone

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
                                           self.InputText, 1)
                            print(cursor.rowcount, "record inserted")
                            cursor.close()
                            self.Done = True

                        else:
                            print("Username already exists. Choose a different username.")
                    elif not self.PasswordDone:
                        # Insert password into the database
                        cursor = conn.cursor()
                        cursor.execute("UPDATE LoginDetails SET Password = ? WHERE Username = ?",
                                       self.PasswordInputText, self.InputText)
                        print(cursor.rowcount, "record updated")
                        cursor.close()
                        self.PasswordDone = True
                        return


                    # cursor = conn.cursor()
                    # cursor.execute(f"insert into {table_name} (Username) VALUES ('{self.InputText}')")
                    # cursor.close()
                    # self.Done = not self.Done
                    # self.entry_complete = True


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



class ExistingUserLogin:
    def __init__(self, x, y, width, height):

        # check if the table exists in the database
        # cursor = conn.cursor()
        # Table_exists = cursor.execute(
        #     f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'")
        # cursor.close()
        # if Table_exists == 0:  # if it does not exist then create the table
        #     cursor = conn.cursor()
        #     cursor.execute(f"CREATE TABLE {table_name}({column_name} varchar(20))")
        #     cursor.close()

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
        return self.InputText, self.Done

    def GetPassword(self):
        return self.PasswordInputText, self.PasswordDone
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
