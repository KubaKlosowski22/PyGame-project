import pygame
import random
import math

# initialize the pygame
pygame.init ()

# create the screen
screen = pygame.display.set_mode ( (800, 600) )

# screen bgc
background = pygame.image.load ( "bgc.jpg" )

# title and icon
pygame.display.set_caption ( "Orc shooter" )
icon = pygame.image.load ( "elf.png" )
pygame.display.set_icon ( icon )

# player character
playerImg = pygame.image.load ( "elf.png" )

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
textY = 10

#game over text

game_over = pygame.font.Font("freesansbold.ttf",64)
# Player - position based on screen size
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
EnemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range ( num_of_enemies ):
    EnemyImg.append ( pygame.image.load ( "orc.png" ) )
    enemyX_change.append ( 2 )
    enemyY_change.append ( 40 )
    enemyX.append ( random.randint ( 0, 735 ) )
    enemyY.append ( random.randint ( 50, 150 )  )

# arrow "ready" - u cant see arrow on the screen
# "fire" - arrow is currently moving

arrowImg = pygame.image.load ( "arrow.png" )
arrowX = 0
arrowY = 480
arrowX_change = 0
arrowY_change = 10
arrow_state = "ready"


# Player character function
def player(x, y, ):
    screen.blit ( playerImg, (x, y) )


def enemy(x, y, i):
    screen.blit ( EnemyImg[i], (x, y) )


def fire_arrow(x, y):
    global arrow_state
    arrow_state = "fire"
    screen.blit ( arrowImg, (x + 16, y + 10) )

def is_collision(enemyX, enemyY, arrowX, arrowY):
    distance = math.sqrt ( (math.pow ( enemyX - arrowX, 2 )) + (math.pow ( enemyY - arrowY, 2 )) )
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Wynik: " + str(score_value),True, (255,255,255))
    screen.blit ( score, (x, y) )

def game_over_text():
    over  = game_over.render("GAME OVER " ,True, (255,255,255))
    screen.blit(over,(200, 250) )
# game loop
running = True
while running:
    # RGB
    screen.fill ( (0, 0, 0) )
    # background image
    screen.blit ( background, (0, 0) )
    for event in pygame.event.get ():
        if event.type == pygame.QUIT:
            running = False

        # Moving spaceship left and right and defining what he do when no left or right clicked
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if arrow_state == "ready":
                    arrowX = playerX
                    fire_arrow ( arrowX, arrowY )
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Character cant move beyond the window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # arrow movement
    if arrowY <= 0:
        arrowY = 480
        arrow_state = "ready"
    if arrow_state == "fire":
        fire_arrow ( arrowX, arrowY )
        arrowY -= arrowY_change

    #bugged not sure how to fix it
    for i in range ( num_of_enemies ):
        #game over
        if enemyY[i] > 440:
            print(enemyY[i])
            for j in range (num_of_enemies):
                enemyY[j] = 801
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collision ( enemyX[i], enemyY[i], arrowX, arrowY )
        if collision:
            arrowY = 480
            arrow_state = "ready"
            score_value += 1
            enemyX[i] = random.randint ( 0, 800 )
            enemyY[i] = random.randint ( 50,150 )

        # enemy calling
        enemy( enemyX[i], enemyY[i], i )

    player ( playerX, playerY )
    show_score(textX,textY)
    pygame.display.update ()
