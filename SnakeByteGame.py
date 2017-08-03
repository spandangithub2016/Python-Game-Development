import pygame
import time
import random

import speech_recognition as sr


pygame.init()

white=(255,255,255)
black=(0,0,0)
red= (255,0,0)
green= (0,155,0)
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Snake Byte Game")


block_size = 20
FPS = 10

AppleThickness= 20

clock = pygame.time.Clock()

#font = pygame.font.SysFont(None, 30)

#declaration of different fonts for game over screen
smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 70)

img = pygame.image.load('snakehead2.png')
appleimg = pygame.image.load('apple.png')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

#pause function screen
def pause():

    paused =  True

    message_to_screen("Game Paused",
                        red,
                        -100,
                        size="large")
    message_to_screen("Press P to play again and Q to quit",
                        green,
                        10)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     #To quit
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:     #To come out of pause screen and play again
                    paused = False
                    
        #gameDisplay.fill(white)
        
        clock.tick(5)
        
        

def score(score):
    points = smallfont.render("Score: " + str(score), True, red)
    gameDisplay.blit(points, [700,0])

#generating randAppleX and randAppleY
def randAppleGen():
    
    randAppleX= round(random.randrange(0, display_width - AppleThickness))
    randAppleY= round(random.randrange(0, display_height - AppleThickness))

    #randAppleX= round(randAppleX/10.0)*10.0
    #randAppleY= round(randAppleY/10.0)*10.0

    return randAppleX, randAppleY

#game Start Screen
def game_intro():

    intro = True
    while intro:
        
        #Events Handling
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:         #To quit
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:         #To play
                    intro = False
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome To The Snake Byte game",
                          green,
                          -100,
                          size="medium")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -10)
        message_to_screen("More apple you ate more you get",
                          black,
                          -40)
        message_to_screen("Press P to play, Q to quit",
                          green,
                          80,
                          "small")
        message_to_screen("Developed By- Spandan Majumder",
                          red,
                          150,
                          "small")
        pygame.display.update()
        clock.tick(5)
    
def snake(block_size, snakeList):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)
    
    #drawing snakeHead image
    gameDisplay.blit(head, (snakeList[-1][0],snakeList[-1][1]))

    #drawing Snake
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay,green,[XnY[0], XnY[1], block_size, block_size])

#module to make text in center
def text_objects(text, color, size):
    
    if size == "small":
        textSurf = smallfont.render(text, True, color)
    if size == "medium":
        textSurf = medfont.render(text, True, color)
    if size == "large":
        textSurf = largefont.render(text, True, color)

    
    return textSurf, textSurf.get_rect()
    

def message_to_screen(msg, color, y_displace=0, size="small"):
    
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2),(display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)

##
##def directions():
##    print("direct fn called")
##    # obtain audio from the microphone
##    r = sr.Recognizer()
##    with sr.Microphone() as source:
##        print("Say something!")
##        audio = r.listen(source)
##    print("start")
##    direction = r.recognize_google(audio)
##    print("Finish")
##    print(direction)
##
##    return direction
##
         
def gameLoop():
    
    global direction        #global declaration for public access
    direction="right"       #initialized bcz when gameLoop run for the first time 
    
    gameExit=False
    gameOver=False
    
    lead_x=300              #left value 
    lead_y=300              #top value
    
    #lead_x_change= 0
    lead_x_change= 10
    lead_y_change= 0

    snakeList=[]
    snakeLength = 1
    

    #Adding an apple to eat
    randAppleX, randAppleY = randAppleGen()

    while not gameExit:
        
        #gameover functionalities
        while gameOver == True:
            gameDisplay.fill(white)
            
            message_to_screen("game Over",
                              red,
                              y_displace = -50,
                              size = "large")
            message_to_screen("press P to play again or Q to quit",
                              black,
                              50,
                              size = "medium")
            
            pygame.display.update()

            #Event Handling in gameover screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit=True
                    gameOver=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit=True
                        gameOver=False
                    if event.key == pygame.K_p:
                        gameLoop()
            
        #Event Handling in game display Screen
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                gameExit=True

##        direction = directions()
##
##        if direction =="left":
##            lead_x_change= -block_size
##            lead_y_change = 0
##        if direction =="right":
##            lead_x_change= block_size
##            lead_y_change = 0            
##        if direction =="up":
##            lead_y_change= -block_size
##            lead_x_change = 0
##        if direction =="down":
##            lead_y_change= block_size
##            lead_x_change = 0
##


            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    #lead_x -=10
                    lead_x_change= -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    #lead_x +=10
                    lead_x_change= block_size
                    lead_y_change = 0
                    
                elif event.key == pygame.K_UP:
                    direction = "up"
                    #lead_y -=10
                    lead_y_change= -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    #lead_y +=10
                    lead_y_change= block_size
                    lead_x_change = 0
                elif event.key == pygame.K_SPACE:
                    pause()

        #if snake reaches surface boundary then die or game over
        if lead_x > display_width or lead_x <0 or lead_y > display_height or lead_y <0:
            gameOver = True
                
        #adding the block and make snake increasing   
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        gameDisplay.fill(white)

        #drawing apple
        #pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))

        #for increasing size of snake
        snakeHead=[]
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        
        if len(snakeList) > snakeLength:
            del snakeList[0]

        #for collision to snake itself
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        #drawing Snake
        snake(block_size,snakeList)

        score(snakeLength - 1)
        
        pygame.display.update()

        #checking that when snake reached a apple that eat the apple
##        if lead_x == randAppleX and lead_y == randAppleY:
##            print("Apple Ate")
##            #Adding an apple to eat
##            randAppleX= random.randrange(0, display_width-block_size)
##            randAppleY= random.randrange(0, display_height-block_size)
##            randAppleX= round(randAppleX/10.0)*10.0
##            randAppleY= round(randAppleY/10.0)*10.0
##            snakeLength += 1

        #checking that snake crashed any1 of the area or portion of the apple (Collision Detection)

        #checking for topLeft by x axis "or" topRight by x axis
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX +  AppleThickness:

            #checking for downLeft by y axis
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

            #checking for downRight by y axis
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
                
        clock.tick(FPS) #frame Per Second
    
    message_to_screen("You Loose", red)
    
    pygame.display.update()
    time.sleep(1)
    
    pygame.quit()
    quit()

game_intro()    #Start Screen Calling
gameLoop()      #game loop calling
