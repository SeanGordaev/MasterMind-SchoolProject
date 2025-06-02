import pygame
import place, Menu
pygame.init()

w, h = 600, 400
display = pygame.display.set_mode((w, h))

main = Menu.MainMenu(display)
#print(Game.Correct)

run = True
while run:
    display.fill((255, 255, 255))

    main.Run()
    main.write()

    #* Detect exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            main.CheckRegisLog(pygame.mouse.get_pos())
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)


Game = place.MainPlace(display)
#The Game
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