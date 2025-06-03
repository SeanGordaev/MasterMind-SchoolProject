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

        self.Nikname = ""
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
                Nikname TEXT,
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
                    self.Nikname = ""
                    self.Password = ""
                    self.CHANGENAME()
                    break
            else: # If user is not exits, then create users
                insert = '''
                INSERT INTO players (Nikname, Password, Points) 
                VALUES (?, ?, ?);
                '''
                player_data = (self.Nikname, self.Password, 0) # New Vlues for table

                # Save and join user into table
                cursor.execute(insert, player_data) 
                connect.commit()

                self.GetData(self.Nikname, self.Password, 0) # Save user as a "currently player"
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
        elif Width_but and Height_but and self.Nikname != "" and self.Password != "":
            Goin = self.GoIn(self.Nikname, self.Password) # Regist / Log in

            return Goin
        return True

    def Run(self):
        Nikname = self.font.render(self.Nikname, True, (0, 0, 0))
        NiknameRect = Nikname.get_rect() 
        NiknameRect.center = tuple(self.FirstInputRect.center)
        self.display.blit(Nikname, NiknameRect)
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
                if not self.PlaceActive and len(self.Nikname) < 15 and not key.isnumeric():
                    self.Nikname += key
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password += key
                self.waiting = 0
            elif keyboard.is_pressed("shift+" + key) and self.waiting > 6 and (key != "backspace"):
                if not self.PlaceActive and len(self.Nikname) < 10:
                    self.Nikname += key.upper()
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password += key.upper()
                self.waiting = 0
            elif keyboard.is_pressed(key) and self.waiting > 6 and key == "backspace":
                if not self.PlaceActive and len(self.Nikname) < 15:
                    self.Nikname = self.Nikname[:len(self.Nikname) - 1]
                elif self.PlaceActive and len(self.Password) < 10:
                    self.Password = self.Password[:len(self.Password) - 1]
                self.waiting = 0
                

class EndMenu:
    def __init__(self):
        pass
