import string, keyboard
import pygame, sqlite3
pygame.init()

class MainMenu:
    def __init__(self, display):
        self.display = display
        self.w = display.get_width()
        self.h = display.get_height()
        pygame.display.set_caption("Menu - login or regist")

        self.keys = [i for i in string.printable[:62]]

        self.nickname = ""
        self.Password = ""
        self.font = pygame.font.Font('freesansbold.ttf', 15)

        self.margin = 5

        self.FirstInputRect = pygame.Rect(0, 0, self.w // 3, self.h // 9)
        self.FirstInputRect.midbottom = (self.w // 2, self.h // 2 - self.margin)

        self.SecondInputRect = pygame.Rect(0, 0, self.w // 4, self.h // 9)
        self.SecondInputRect.midtop = (self.w // 2, self.h // 2 + self.margin)

        self.button = pygame.Rect(0, 0, self.w // 5, self.h // 9)
        self.button.center = (self.SecondInputRect.centerx, self.SecondInputRect.centery + self.h // 9 + self.margin)

        self.PlaceActive = False

        self.waiting = 0 # Stop Time between pressing on the buttons

    def CHANGENAME(self):
        ...
    
    def GetData(self, N, P, Po):
        with open("BASE\CURR.txt", "w") as file:
            file.write(f"{N}:{P}:{Po}")
    
    def GoIn(self, Name, Password):

        #    Name      |   Password     |    Points
        # USERNAME_1  | USERPASSWORD_1 | USERPOINTS_1
        # USERNAME_2 | USERPASSWORD_2 | USERPOINTS_2

        with sqlite3.connect('BASE\playersDataBase.db') as connect:
            cursor = connect.cursor()

            #* Create table players - if it is not exits \------------------------------
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                nickname TEXT,
                Password TEXT,
                Points INTEGER     
            );
            """)
            connect.commit()


            #* Regist / Log in Player \------------------------------
            cursor.execute("""SELECT * FROM players""")
            all_players = cursor.fetchall() # Get list of All players

            for player in all_players:
                if player[0] == Name and player[1] == Password: # If name user exists and password is correct
                    self.GetData(player[0], player[1], player[2])  # Save user as a "currently player"
                    return False
                elif player[0] == Name: # If name user exists, but password isn't correct
                    self.nickname = ""
                    self.Password = ""
                    self.CHANGENAME()
                    break
            else: # If user is not exits, then create users
                insert = '''
                INSERT INTO players (nickname, Password, Points) 
                VALUES (?, ?, ?);
                '''
                player_data = (self.nickname, self.Password, 0) # New Vlues for table

                # Save and join user into table
                cursor.execute(insert, player_data) 
                connect.commit()

                self.GetData(self.nickname, self.Password, 0) # Save user as a "currently player"
                return False
        
        return True


    def CheckRegisLog(self, pos):
        Width_First = self.FirstInputRect.x <= pos[0] <= self.FirstInputRect.x + self.FirstInputRect.w
        Height_First = self.FirstInputRect.y <= pos[1] <= self.FirstInputRect.y + self.FirstInputRect.h

        Width_Second = self.SecondInputRect.x <= pos[0] <= self.SecondInputRect.x + self.FirstInputRect.w
        Height_Second = self.SecondInputRect.y <= pos[1] <= self.SecondInputRect.y + self.FirstInputRect.h

        Width_but = self.button.x <= pos[0] <= self.button.x + self.button.w
        Height_but = self.button.y <= pos[1] <= self.button.y + self.button.h

        if Width_First and Height_First:
            self.PlaceActive = False
        elif Width_Second and Height_Second:
            self.PlaceActive = True
        elif Width_but and Height_but and self.nickname != "" and self.Password != "":
            Goin = self.GoIn(self.nickname, self.Password) # Regist / Log in

            return Goin
        return True

    def Run(self):
        nickname = self.font.render(self.nickname, True, (0, 0, 0))
        nicknameRect = nickname.get_rect() 
        nicknameRect.center = tuple(self.FirstInputRect.center)
        self.display.blit(nickname, nicknameRect)
        pygame.draw.rect(self.display, (10, 10, 10), self.FirstInputRect, 3, 4)

        Password = self.font.render(self.Password, True, (0, 0, 0))
        PasswordRect = Password.get_rect() 
        PasswordRect.center = tuple(self.SecondInputRect.center)
        self.display.blit(Password, PasswordRect)
        pygame.draw.rect(self.display, (10, 10, 10), self.SecondInputRect, 3, 4)

        text = self.font.render("Go in", True, (255, 255, 255))
        textRect = text.get_rect() 
        textRect.center = tuple(self.button.center)
        pygame.draw.rect(self.display, (50, 50, 50), self.button, 0, 6)
        pygame.draw.rect(self.display, (10, 10, 10), self.button, 3, 4)
        self.display.blit(text, textRect)

        self.waiting += 1


    def write(self):
        for key in self.keys + ["backspace"]:
            if keyboard.is_pressed(key) and self.waiting > 6 and (not keyboard.is_pressed("shift")) and (key != "backspace"):
                if not self.PlaceActive and len(self.nickname) < 15 and not key.isnumeric():
                    self.nickname += key
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password += key
                self.waiting = 0
            elif keyboard.is_pressed("shift+" + key) and self.waiting > 6 and (key != "backspace"):
                if not self.PlaceActive and len(self.nickname) < 10:
                    self.nickname += key.upper()
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password += key.upper()
                self.waiting = 0
            elif keyboard.is_pressed(key) and self.waiting > 6 and key == "backspace":
                if not self.PlaceActive and len(self.nickname) < 15:
                    self.nickname = self.nickname[:len(self.nickname) - 1]
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password = self.Password[:len(self.Password) - 1]
                self.waiting = 0
                

class EndMenu:
    def __init__(self, display):
        self.display = display
        self.w = display.get_width()
        self.h = display.get_height()
        pygame.display.set_caption("End - Thank for game")

        self.font = pygame.font.Font('freesansbold.ttf', 30)

        self.Tags = ("nickname", "Point (After Game)", "Added after Game")
        try:
            with open("BASE\CURR.txt", "r") as file:
                self.Data = file.readline().split(":")
                self.Data.pop(1)
        except (ValueError):
            self.Data = ("KELO", "10", "10", "Lost")
        
        

        #* Player Data
        # Name
        self.Name, self.NameRect = self.AddText(self.Data[0], self.font, (1 * self.w / 7, self.h / 2))
        # Point
        self.Point, self.PointRect = self.AddText(f"Point:{self.Data[1]}", self.font, (3.5 * self.w / 7, self.h / 2))
        # Added
        self.Added, self.AddedRect = self.AddText(f"added:+{self.Data[2]}", self.font, (6 * self.w / 7 - 5, self.h / 2))
        #Data PLace
        self.Place = pygame.Rect(self.NameRect.x - 10, self.NameRect.y - 10, self.AddedRect.bottomright[0] - self.NameRect.x + 15, self.AddedRect.bottomright[1] - self.NameRect.y + 20)
        #Status
        self.Status, self.StatusRect = self.AddText(self.Data[3], pygame.font.Font('freesansbold.ttf', 50), (self.w / 2, self.h / 4))


    def AddText(self, text: str, font: pygame.font.Font, center) -> list[str]: # set setting for write on display
        text = font.render(text, True, (0, 0, 0))
        textRect = text.get_rect() 
        textRect.center = center

        return text, textRect

    def Run(self):
        pygame.draw.rect(self.display, (0, 0, 0), self.Place, 3, 4)
        
        self.display.blit(self.Name, self.NameRect)
        # Point
        self.display.blit(self.Point, self.PointRect)
        # Added
        self.display.blit(self.Added, self.AddedRect)
        # WInLost
        self.display.blit(self.Status, self.StatusRect)


