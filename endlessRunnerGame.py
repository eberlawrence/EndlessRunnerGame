import pygame

pygame.init()

display_width = 800
display_height = 600
bat_width = 55

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

batImg1 = pygame.image.load('images/bat1.png')
batImg2 = pygame.image.load('images/bat2.png')


def bat(img1, x, y):
    gameDisplay.blit(img1, (x, y))


def loop():
    flag = True
    count = 0
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change, y_change = 0, 0

    crash = False
    while not crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -55
            if event.key == pygame.K_RIGHT:
                x_change = 55        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
        
        x += x_change

        gameDisplay.fill(white)

        if flag == True:
            bat(batImg1, x, y)
            count += 1
            if count == 25: 
                flag = False
                count = 0
        else:
            bat(batImg2, x, y)
            count += 1
            if count == 15: 
                flag = True
                count = 0
    
        if x > display_width - bat_width or x < 0:
            crash = True
            
        pygame.display.update()
        clock.tick(60)

loop()
pygame.quit()
quit()



