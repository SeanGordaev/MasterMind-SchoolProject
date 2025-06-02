import string, keyboard
import pygame
pygame.init()

class MainMenu:
    def __init__(self, display):
        self.display = display
        self.w = display.get_width()
        self.h = display.get_height()
        pygame.display.set_caption("Menu - login or regist")

        self.keys = [i for i in string.printable[:62]]
        print(self.keys)

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
    
    def GoIn(self):

        #    Name      |   Password     |    Points
        # USERNAME_1  | USERPASSWORD_1 | USERPOINTS_1
        # USERNAME_2 | USERPASSWORD_2 | USERPOINTS_2

        #Todo Make Regist / Log in user to system
        ...

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
        elif Width_but and Height_but:
            print("--In Work--")
            self.GoIn() # Regist / Log in

        

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
                

        

