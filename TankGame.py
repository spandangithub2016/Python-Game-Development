import pygame
import time
import random

pygame.init()

white=(255,255,255)
black=(0,0,0)

red= (200,0,0)
light_red= (255,0,0)

green= (34,177,76)
light_green= (0,255,0)

yellow= (200,200,0)
light_yellow= (255,255,0)

display_width = 800
display_height = 600

tankwidth = 40
tankheight = 20

turretWidth = 5
wheelWidth = 5

ground_height = 35

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Tank Game")

#one = pygame.image.load("bg1.jpg")
#gameStartImage = pygame.image.load("gameStart.jpg")
two = pygame.image.load("gameIntro.jpg")


player_fire_sound = pygame.mixer.Sound("fire1.wav")
enemy_fire_sound = pygame.mixer.Sound("fire2.wav")
sample1_fire_sound = pygame.mixer.Sound("fire3.wav")
player_explosion_sound = pygame.mixer.Sound("Explosion1.wav")
enemy_explosion_sound = pygame.mixer.Sound("Explosion2.wav")

block_size = 20

clock = pygame.time.Clock()

#font = pygame.font.SysFont(None, 30)

#declaration of different fonts for game over screen
smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 40)
largefont = pygame.font.SysFont("comicsansms", 70)

#img = pygame.image.load('snakehead2.png')
#appleimg = pygame.image.load('apple.png')

#icon = pygame.image.load('apple.png')
#pygame.display.set_icon(icon)

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
   
#module to make text in center
def text_objects(text, color, size):
    
    if size == "small":
        textSurf = smallfont.render(text, True, color)
    if size == "medium":
        textSurf = medfont.render(text, True, color)
    if size == "large":
        textSurf = largefont.render(text, True, color)

    return textSurf, textSurf.get_rect()


def text_to_button(msg,color,buttonx,buttony,buttonwidth,buttonheight,size= "small"):
    
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), (buttony + (buttonheight / 2)))
    gameDisplay.blit(textSurf,textRect)

def button(text, x, y, width, height, inactive_color, active_color, action = None):

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))

        if click[0] == 1 and action != None:
            if action == "play":
                gameLoop()
            if action == "controls":
                game_controls()
            if action == "quit":
                pygame.quit()
                quit()
            if action == "main":
                game_intro()    
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))
        
    text_to_button(text, black, x, y, width, height)
    

def message_to_screen(msg, color, y_displace=0, size="small"):
    
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2),(display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)


def tank(x,y,turPos):
    
    x = int(x)
    y = int(y)

    possibleTurrets = [ (x-27, y-2),
                        (x-26, y-5),
                        (x-25, y-8),
                        (x-23, y-12),
                        (x-20, y-14),
                        (x-18, y-15),
                        (x-15, y-17),
                        (x-13, y-19),
                        (x-11, y-21)
                    ]

    #Tank Body
    pygame.draw.circle(gameDisplay, black, (x,y), int(tankheight / 2))
    pygame.draw.rect(gameDisplay, black, (x-tankheight, y, tankwidth, tankheight))

    #To draw Turret
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

    #To draw wheels
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)

    return possibleTurrets[turPos]

def enemy_tank(x,y,turPos):

    x = int(x)
    y = int(y)

    possibleTurrets = [ (x+27, y-2),
                        (x+26, y-5),
                        (x+25, y-8),
                        (x+23, y-12),
                        (x+20, y-14),
                        (x+18, y-15),
                        (x+15, y-17),
                        (x+13, y-19),
                        (x+11, y-21)
                    ]

    #Tank Body
    pygame.draw.circle(gameDisplay, black, (x,y), int(tankheight / 2))
    pygame.draw.rect(gameDisplay, black, (x-tankheight, y, tankwidth, tankheight))

    #To draw Turret
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)

    #To draw wheels
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)

    return possibleTurrets[turPos]


def barrier(xlocation, randomHeight,barrier_width):

    pygame.draw.rect(gameDisplay, black, [xlocation, display_height - randomHeight, barrier_width, randomHeight])

def explosion(x, y, size=50, player="x"):

    if player == "player":
        pygame.mixer.Sound.play(player_explosion_sound)
    elif player == "enemy":
        pygame.mixer.Sound.play(enemy_explosion_sound)
    else:
        pass
        
    explode = True
    
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = x,y
        colorChoices = [red, green, yellow, light_green, light_red, light_yellow]
        magnitude = 1
        
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)
            
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)

        explode = False          

def fireShell2(xy, tankx, tanky, turPos, gun_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY):

    song_number = random.randrange(0,2)
    if song_number == 0:
        pygame.mixer.Sound.play(player_fire_sound)
    else:
        pygame.mixer.Sound.play(sample1_fire_sound)
        
    fire = True
    damage = 0
    startingShell = list(xy) 
    
    while fire:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #print(startingShell[0], startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

        startingShell[0] -= (12 - turPos) * 2

        #y = x**2
        startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(gun_power/30))**2)-(turPos+turPos/(12-turPos)))
        
        if startingShell[1] > display_height - ground_height:
            hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
            hit_y = int(display_height - ground_height)

            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                print("Critical Hit!")
                damage = 25
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                print("Hard Hit!")
                damage = 18
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                print("Medium Hit!")
                damage = 10
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                print("Light Hit!")
                damage = 5

            explosion(hit_x, hit_y, player = "player")
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight
        
        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            #to explosion bariiers by gun
            explosion(hit_x, hit_y)
            fire = False
    

        pygame.display.update()
        clock.tick(50)
    return damage


def e_fireShell2(xy, tankx, tanky, turPos, gun_power, xlocation, barrier_width, randomHeight, ptankx, ptanky):

    song_number = random.randrange(0,2)
    if song_number == 0:
        pygame.mixer.Sound.play(enemy_fire_sound)
    else:
        pygame.mixer.Sound.play(sample1_fire_sound)
    
    damage = 0
    currentPower = 1
    power_found = False

    while not power_found:

        
        currentPower += 1
        if currentPower > 78:
            power_found = True
        fire = True
        
        startingShell = list(xy) 
        
        while fire:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            startingShell[0] += (12 - turPos) * 2

            #y = x**2
            startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(currentPower/50.5))**2)-(turPos+turPos/(12-turPos)))
            
            if startingShell[1] > display_height - ground_height:
                hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
                hit_y = int(display_height - ground_height)

                if ptankx + 15 > hit_x > ptankx - 15:
                    power_found ==  True
                    
                fire = False

            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation
            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight
            
            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                fire = False
    

    fire = True
    startingShell = list(xy) 
    
    while fire:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #print(startingShell[0], startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)

        startingShell[0] += (12 - turPos) * 2

        #y = x**2
        gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.10))
        startingShell[1] += int((((startingShell[0] - xy[0])*0.015/(gun_power/49.5))**2)-(turPos+turPos/(12-turPos)))
        
        if startingShell[1] > display_height - ground_height:
            hit_x = int((startingShell[0]*display_height - ground_height)/startingShell[1])
            hit_y = int(display_height - ground_height)
            
            if ptankx + 10 > hit_x > ptankx - 10:
                print("Critical Hit!")
                damage = 25
            elif ptankx + 15 > hit_x > ptankx - 15:
                print("Hard Hit!")
                damage = 18
            elif ptankx + 25 > hit_x > ptankx - 25:
                print("Medium Hit!")
                damage = 10
            elif ptankx + 35 > hit_x > ptankx - 35:
                print("Light Hit!")
                damage = 5

            
            #to explosion bariiers by gun
            explosion(hit_x, hit_y, player = "enemy")
            fire = False

        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight
        
        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            #to explosion bariiers by gun
            explosion(hit_x, hit_y,  player = "enemy")
            fire = False

        

        pygame.display.update()
        clock.tick(50)

    return damage

        
def game_controls():

    gcont = True
    while gcont:
        
        #Events Handling
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                   
        gameDisplay.blit(two, [0,0])
        message_to_screen("Controls",
                          green,
                          -120,
                          size="large")
        message_to_screen("Fire : spacebar",
                          white,
                          -50)
        message_to_screen("Move Turret: Up and Down Arrows",
                          white,
                          -15)
        message_to_screen("Move Tank: Left and Right Arrows",
                          white,
                          20)
        message_to_screen("Pause: P",black,45)

        button("Play", 150, 380, 100, 50, green, light_green, action = "play")
        button("Main Menu", 350, 380, 100, 50, yellow, light_yellow, action = "main")
        button("Quit", 550, 380, 100, 50, red, light_red, action = "quit")
        
        pygame.display.update()
        clock.tick(5)

def power(level):

    text = smallfont.render("Power: " + str(level) + "%", True, red)
    gameDisplay.blit(text, [display_width / 2, 0])


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
                    
        gameDisplay.blit(two, [-200,-200])
        message_to_screen("Welcome To The Tanks game", green, -100, size="medium")
        message_to_screen("The objective of the game is to Shoot and Destroy", white, -10)
        message_to_screen("More enemies you destroy , harder they get",white,-40)
        button("Play", 150, 350, 100, 50, green, light_green, action = "play")
        button("Controls", 350, 350, 100, 50, yellow, light_yellow, action = "controls")
        button("Quit", 550, 350, 100, 50, red, light_red, action = "quit")
        message_to_screen("Developed By- Spandan Majumder",red,150,"small")
        
        pygame.display.update()
        clock.tick(5)


#game Over Screen
def game_over():

    gameDisplay.blit(two, [0,0])
    game_over = True
    while game_over:
        
        #Events Handling
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        message_to_screen("Game Over", green, -100, size="medium")                
        message_to_screen("You Died", black, -10)        
        message_to_screen("More enemies you destroy , harder they get",black,-40)

        button("Play Again", 150, 350, 100, 50, green, light_green, action = "play")
        button("Controls", 350, 350, 100, 50, yellow, light_yellow, action = "controls")
        button("Quit", 550, 350, 100, 50, red, light_red, action = "quit")
        
        pygame.display.update()
        clock.tick(5)

#Winning Screen
def you_win():

    win = True
    while win:
        
        #Events Handling
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        message_to_screen("You Won!", green, -100, size="medium")
        message_to_screen("Congratulations!", black, -10)

        button("Play Again", 150, 350, 100, 50, green, light_green, action = "play")
        button("Controls", 350, 350, 100, 50, yellow, light_yellow, action = "controls")
        button("Quit", 550, 350, 100, 50, red, light_red, action = "quit")
        
        pygame.display.update()
        clock.tick(5)

def health_bars(player_health, enemy_health):

    #Player Health
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red

    #Enemy Health
    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red

    pygame.draw.rect(gameDisplay, player_health_color, (680, 10, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (25, 10, enemy_health, 25))
        
    
def gameLoop():
    
    #Background Music
    pygame.mixer.music.load("battle-war.wav")
    pygame.mixer.music.play(-1)

    gameExit=False
    gameOver=False
    FPS = 15

    player_health = 100
    enemy_health = 100

    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    currentTurPos = 0
    changeTur = 0

    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9

    xlocation = (display_width / 2) + random.randint(-0.1 * display_width, 0.1 * display_width)
    randomHeight = random.randrange(display_height * 0.1, display_height * 0.5)

    barrier_width = 50
    fire_power = 50
    power_change = 0

    while not gameExit:


        #gameover functionalities
        while gameOver == True:
            gameDisplay.fill(white)
            
            message_to_screen("game Over", red, y_displace = -50, size = "large")
            message_to_screen("press P to play again or Q to quit", black, 50, size = "medium")
            
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove  = -5
                
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                    
                elif event.key == pygame.K_UP:
                    changeTur = 1
                
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                
                elif event.key == pygame.K_SPACE:
                    pause()
                    
                elif event.key == pygame.K_f:
                    damage = fireShell2(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY)
                    enemy_health -= damage

                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)
                    
                    for x in range(random.randrange(0,10)):
                      
                        if display_width * 0.3 > enemyTankX > display_width * 0.03:
                            
                            if possibleMovement[moveIndex] == 'f':
                                enemyTankX += 5
                                
                            elif possibleMovement[moveIndex] == 'r':
                                enemyTankX -= 5

                            gameDisplay.blit(two, [0,0])

                            health_bars(player_health, enemy_health)        

                            gun = tank(mainTankX, mainTankY, currentTurPos)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)

                            fire_power += power_change
                            power(fire_power)
                            barrier(xlocation, randomHeight, barrier_width)
                            
                            #draw ground color
                            gameDisplay.fill(black, rect =[0, display_height - ground_height, display_width, ground_height])

                            pygame.display.update()
                            clock.tick(FPS)

                    damage = e_fireShell2(enemy_gun, enemyTankX, enemyTankY, 8, 50, xlocation, barrier_width, randomHeight, mainTankX, mainTankY)
                    player_health -= damage
                    
                elif event.key == pygame.K_a:
                    power_change = -1
                    
                elif event.key == pygame.K_d:
                    power_change = 1




                    
            #for preventing to moving continue
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove  = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0

                    
                    
        #move Tank
        mainTankX += tankMove

        #move Turret/Gun
        currentTurPos += changeTur

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 8

        if mainTankX - (tankwidth / 2) < xlocation + barrier_width:
            mainTankX += 5

        gameDisplay.blit(two, [0,0])

        health_bars(player_health, enemy_health)        
        gun = tank(mainTankX, mainTankY, currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
        
        fire_power += power_change

        #Setting power maximum 100% and minimum 1%
        if fire_power > 100:
            fire_power = 100
        elif fire_power< 1:
            fire_power = 1
        
        power(fire_power)
        
        #to make Barrier
        barrier(xlocation, randomHeight, barrier_width)
        
        #to draw ground
        gameDisplay.fill(black, rect =[0, display_height - ground_height, display_width, ground_height])

        pygame.display.update()

        if player_health < 1:
            game_over()
        elif enemy_health < 1:
            you_win()

        clock.tick(FPS)         #frame Per Second

    pygame.quit()
    quit()

game_intro()    #Start Screen Calling
gameLoop()      #game loop calling
