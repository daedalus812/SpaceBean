import math
import random

import pygame
from pygame import mixer

# Inizialzizo PyGame
pygame.init()

# Configuro la schermata
screen = pygame.display.set_mode((800, 600))

# Sfondo
background = pygame.image.load('background.png')

# Musiche
mixer.music.load("background.wav")
mixer.music.play(-1)

# Titolo ed icona della finestra
pygame.display.set_caption("SPACEBEAN")
icon = pygame.image.load('mrbean.png')
pygame.display.set_icon(icon)

# Giocatore
playerImg = pygame.image.load('giocatore.png')
playerX = 370
playerY = 480
playerX_change = 0

# Nemico
nemicopng = []
nemicoX = []
nemicoY = []
nemicoX_var = []
nemicoY_var = []
num_nemici = 6

for i in range(num_nemici):
    nemicopng.append(pygame.image.load('nemici.png'))
    nemicoX.append(random.randint(0, 736))
    nemicoY.append(random.randint(50, 150))
    nemicoX_var.append(4)
    nemicoY_var.append(40)

# Proiettile

# Ready - Il proiettile non compare nello schermo
# Fire - Il proiettile comincia a muoversi

proiettilepng = pygame.image.load('proiettile.png')
proiettileX = 0
proiettileY = 480
proiettileX_var = 0
proiettileY_var = 10
stato_proiettile = "ready"

# Punteggio

punteggio = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def mostra_punteggio(x, y):
    punteggiox = font.render("Punti: " + str(punteggio), True, (255, 255, 255))
    screen.blit(punteggiox, (x, y))

def firma(x, y):
    firma = font.render("Lorenzo Fanelli, MAT 234339", True, (255, 255, 255))
    screen.blit(firma, (x, y))


def scritta_game_over():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def giocatore(x, y):
    screen.blit(playerImg, (x, y))


def nemico(x, y, i):
    screen.blit(nemicopng[i], (x, y))


def proiettileT(x, y):
    global stato_proiettile
    stato_proiettile = "fire"
    screen.blit(proiettilepng, (x + 16, y + 10))


def CollisioneT(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Loop
running = True
while running:

    # RGB = Rosso, Verde, Blu
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if stato_proiettile == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    proiettileX = playerX
                    proiettileT(proiettileX, proiettileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Movimento del nemico
    for i in range(num_nemici):

        # Game Over
        if nemicoY[i] > 440:
            for j in range(num_nemici):
                nemicoY[j] = 2000
            scritta_game_over()
            break

        nemicoX[i] += nemicoX_var[i]
        if nemicoX[i] <= 0:
            nemicoX_var[i] = 4
            nemicoY[i] += nemicoY_var[i]
        elif nemicoX[i] >= 736:
            nemicoX_var[i] = -4
            nemicoY[i] += nemicoY_var[i]

        # Collisione
        collisione = CollisioneT(nemicoX[i], nemicoY[i], proiettileX, proiettileY)
        if collisione:
            esplosionewav = mixer.Sound("explosion.wav")
            esplosionewav.play()
            proiettileY = 480
            stato_proiettile = "ready"
            punteggio += 1
            nemicoX[i] = random.randint(0, 736)
            nemicoY[i] = random.randint(50, 150)

        nemico(nemicoX[i], nemicoY[i], i)

    # Movimento del proiettile
    if proiettileY <= 0:
        proiettileY = 480
        stato_proiettile = "ready"

    if stato_proiettile == "fire":
        proiettileT(proiettileX, proiettileY)
        proiettileY -= proiettileY_var

    giocatore(playerX, playerY)
    mostra_punteggio(textX, testY)
    firma(320,10)
    pygame.display.update()