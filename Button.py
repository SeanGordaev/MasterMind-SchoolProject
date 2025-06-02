import pygame

class Button:
    def __init__(self, root, color, W, H, positionOn: list[int] | tuple[int] = (0, 0), positionBy: str = "center", widthLine: int = -1, border: int = -1):
        self.root = root
        self.color = color
        self.widthLine = widthLine
        self.border = border

        if positionBy == "center":
            self.Rect = pygame.Rect(0, 0, W, H)
            self.Rect.center = (positionOn[0], positionOn[1])

        #todo - Add position by other point: button, up, left, right and more
    
    def Draw(self):
        pygame.draw.rect(self.root, self.color, self.Rect, self.widthLine, self.border)

    def Is_Pressed(self, MousePos: list[int] | tuple[int]):
        X = self.Rect.x <= MousePos[0] <= self.Rect.x + self.Rect.width
        Y = self.Rect.y <= MousePos[1] <= self.Rect.y + self.Rect.height

        if X and Y:
            return True
        return False