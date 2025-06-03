import pygame, keyboard, random
import Button
pygame.init()

class MainPlace:
    def __init__(self, display):
        self.display = display
        self.w = display.get_width()
        self.h = display.get_height()
        pygame.display.set_caption("Games")

        #* Game setting
        self.Lenght = 4
        self.Guess = [] # Place for guess Numbers | user
        self.Keys = ("1", "2", "3") #tuple(string.digits)[:7] # Array of 0 - 6 (include) | zero only if user wants to delete
        self.Acts = ("0", "4") # for delete and add
        self.Correct = [] # Place for correct numbers | Game
        while len(self.Correct) < self.Lenght:                                  # | Create the line of numbers
            Rand_Num = str(random.randint(1, int(max(self.Keys))))              # |
            self.Correct.append(Rand_Num)                                       # |
        self.attempts = 35

        #* Setting for Text 
        self.fontSize = 50
        self.font = pygame.font.Font('freesansbold.ttf', self.fontSize) # Font for text

        #* Widget
        margin = 5
        TakeCol = self.w - margin
        TakeRow = self.h - margin
        self.GamePlace = pygame.Rect(self.w / TakeCol + margin, self.h / TakeRow + margin, (TakeCol - 1) * self.w / TakeCol - (margin * 2), self.h * (TakeRow - 1) / TakeRow - (margin * 2))

        self.Bt = Button.Button(display, (0, 0, 0), 120, 35, (self.GamePlace.centerx, self.GamePlace.centery + 55), widthLine = 3, border = 5)

        #* flags
        self.mDelete = False # for Detect if user try delete something
        self.mAdd = False # Detect if user try add number on some-index
        self.AddTo = None # To know where add number after "enter"
        self.flag = True # Protect user - stop spam of letters
        self.TimeOut = 0

        #* Messages
        self.mCorrect_place = self.mWrong_place = None
        self.t = self.m = None
        self.mToEnd = {
            1: lambda x: f"{x}th is correct, but not in correct place", # wrong places
            2: lambda x: f"{x}th is correct and in correct place", # correct places
            3: lambda x, y: f"{x}th in correct place, {y}th not in correct place", # correct and wrong places
            5: lambda: "No one is correct", # No one is correct
        }
        self.mPos = (self.GamePlace.centerx, 5 * self.GamePlace.centery / 3)


    def AddText(self, Guess: str, font: pygame.font.Font, center) -> list[str]: # set setting for write on display
        text = font.render(Guess, True, (0, 0, 0))
        textRect = text.get_rect() 
        textRect.center = center

        return text, textRect


    def NextTimeout(self):
        if self.TimeOut > 10:
            self.TimeOut = 0
            self.flag = True
        else:
            self.TimeOut += 1


    def Check_guess(self, Guess: list, Correct: list) -> tuple[int]:
        if Guess == Correct:
            return (-1, -1)
        else:
            Correct_Place = 0
            Wrong_Place = 0

            Correct_copy = Correct.copy()
            Guess_copy = Guess.copy()

            for ind, gValue in enumerate(Guess):
                if gValue == Correct[ind]: # if the same value from the user's Guess is in the same index in the "correct"
                    Correct_Place += 1
                    Guess_copy[ind] = Correct_copy[ind] = None
            
            for ind, gValue in enumerate(Guess):
                if (Guess_copy[ind] != None) and (gValue in Correct_copy):
                    Wrong_Place += 1
            

        return Correct_Place, Wrong_Place

    def MainLoop(self):
        #! main control \-------------------------------
        #* Detect pressed on keyboard || add 1 or 2 at the end, delete at index, add at index
        #*---# Add at the end, delete  and add at the index
        for key in (self.Keys + self.Acts):
            if (keyboard.is_pressed(key)) and (self.flag): # get number of keys: 1 - 3
                if (not self.mDelete) and (not self.mAdd) and (key in self.Keys) and (len(self.Guess) < self.Lenght) and (int(key) > 0): # Add number at the end
                    self.Guess.append(key)

                elif self.mDelete: # Delete number at the index
                    if int(key) == 0: # if user chooses 0 all his guess clear
                        self.Guess.clear()
                    else:
                        if (int(key) - 1 < len(self.Guess)):
                            self.Guess.pop(int(key) - 1)
                    self.mDelete = False

                elif self.mAdd: # Add number at the index
                    if (not isinstance(self.AddTo, int)) and (int(key) - 1 < len(self.Guess)): # get index where add number
                        self.AddTo = int(key) - 1
                        self.W, self.R = self.AddText(f"Choice number (1 - 9)", pygame.font.Font('freesansbold.ttf', self.fontSize // 2), (self.GamePlace.centerx , self.GamePlace.centery - self.fontSize))
                    elif (isinstance(self.AddTo, int)): # get number to added at the index
                        self.Guess.insert(self.AddTo, key)
                        self.AddTo = None
                        self.mAdd = False
                
                #---# Fot timeout and stop spam writing
                self.flag = False
                self.TimeOut = 0

        #*---# hotkey -> delete, add, exit from their, auto win
        if (keyboard.is_pressed("backspace")) and (self.flag) and (not self.mDelete) and (len(self.Guess) > 0): # detect for delete
            self.W, self.R = self.AddText(f"Choice index (1 - {len(self.Guess)}) or press 0 for all - Delete", pygame.font.Font('freesansbold.ttf', self.fontSize // 3), (self.GamePlace.centerx, self.GamePlace.centery - self.fontSize * 1.25))
            self.mDelete = True # now "delete at index" on
            
            #---# Fot timeout and stop spam writing
            self.flag = False
            self.TimeOut = 0
        elif (keyboard.is_pressed("enter")) and (self.flag) and (not self.mAdd) and (0 < len(self.Guess) < self.Lenght): # detect for add
            self.W, self.R = self.AddText(f"Choice index (1 - {len(self.Guess)}) - Add", pygame.font.Font('freesansbold.ttf', self.fontSize // 3), (self.GamePlace.centerx , self.GamePlace.centery- self.fontSize * 1.25))
            self.mAdd = True # now "Add at index" on

            #---# Fot timeout and stop spam writing
            self.flag = False
            self.TimeOut = 0
        elif (keyboard.is_pressed("esc")): # esc. from delete and add
            self.mAdd = False
            self.mDelete = False
        elif (keyboard.is_pressed("m")):
            return False

        #*---# add messages on display when user: delete / add
        if self.mDelete or self.mAdd:
            self.display.blit(self.W, self.R)

        #! Draw on display || text, rect around the text
            # Write the Guess on display
        text = ''.join(self.Guess)
        Write, WriteReact = self.AddText(text, self.font, self.GamePlace.center)
        self.display.blit(Write, WriteReact)
        
            # Draw a notion place
        #pygame.draw.rect(self.display, (50, 50, 50), self.Noite)

            # Draw rect around the text
        rect_Around_Text = pygame.Rect(0, 0, self.font.size(text)[0] + 10, self.font.size(text)[1] + 5)
        rect_Around_Text.center = self.GamePlace.center
        pygame.draw.rect(self.display, (0, 0, 0), rect_Around_Text, 3, 6)

            # Draw witget
        self.Bt.Draw() # button

            # Draw around the place of game
        pygame.draw.rect(self.display, (0, 0, 0), self.GamePlace, 4, 4)

            # Drawn attempts
        Atte, AtteReact = self.AddText(str(self.attempts), self.font, (0, 0))
        AtteReact.topleft = (self.GamePlace.x + 5, self.GamePlace.y + 5)
        self.display.blit(Atte, AtteReact)

        #! Check user's Guess 
        if pygame.mouse.get_pressed()[0] and self.Bt.Is_Pressed(pygame.mouse.get_pos()) and len(self.Guess) == self.Lenght: # if user click on the button
            Is_correct = self.Check_guess(self.Guess, self.Correct)

            if Is_correct == (-1, -1) or self.attempts == 0:

                with open("BASE\CURR.txt", "r") as file:
                    Name, Password, Point = file.readline().split(":")
                    Point = int(Point)
                with open("BASE\CURR.txt", "w") as file:
                    if self.attempts == 0:
                        file.write(f"{Name}:{Password}:{Point + self.attempts}:lost")
                    else:
                        file.write(f"{Name}:{Password}:{Point + self.attempts}:win")

                return False # end game
            else:
                if Is_correct == (0, 0): 
                    self.t, self.m = self.AddText(self.mToEnd[5](), pygame.font.Font('freesansbold.ttf', self.fontSize // 3), self.mPos)
                else:
                    if Is_correct[0] != 0 and Is_correct[1] != 0:
                        self.t, self.m = self.AddText(self.mToEnd[3](Is_correct[0], Is_correct[1]), pygame.font.Font('freesansbold.ttf', self.fontSize // 3), self.mPos)
                    elif Is_correct[0] != 0:
                        self.t, self.m = self.AddText(self.mToEnd[2](Is_correct[0]), pygame.font.Font('freesansbold.ttf', self.fontSize // 3), self.mPos)
                    elif Is_correct[1] != 0:
                        self.t, self.m = self.AddText(self.mToEnd[1](Is_correct[1]), pygame.font.Font('freesansbold.ttf', self.fontSize // 3), self.mPos)
                if self.flag:
                    self.attempts -= 1 # user lost one attempt
                    self.flag = False
                    self.TimeOut = 0

        if (self.t != None and self.m != None):
            self.display.blit(self.t, self.m)
        
        # continue game
        return True

