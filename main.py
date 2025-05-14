import pygame
import place
pygame.init()

w, h = 600, 400
display = pygame.display.set_mode((w, h))

Game = place.MainPlace(display, w, h)
#print(Game.Correct)
print(Game.Correct)
run = True
while run:
    display.fill((255, 255, 255))
    Game.NextTimeout()
        
    run = Game.MainLoop()

    #* Detect exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    pygame.display.update()
    pygame.time.Clock().tick(60)
pygame.quit()