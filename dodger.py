import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
MONSTERINSIZE = 10
MONSTERMAXSIZE = 40
MONSTERMINSPEED = 1
MONSTERMAXSPEED = 8
ADDNEWMONSTERRATE = 6
DOGMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForDogToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def dogHasHitMonster(dogRect,monsters ):
    for b in monsters :
        if dogRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)


gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')


dogImage = pygame.transform.scale(pygame.image.load('dog.png'),(40,40))
dogRect = dogImage.get_rect()
monsterImage = pygame.image.load('monster.png')

drawText('Втікай або програєш', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Ви починаєте гру.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForDogToPressKey()


topScore = 0
while True:

    monsters = []
    score = 0
    dogRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    monsterAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: 
        score += 1 

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                dogRect.move_ip(event.pos[0] - dogRect.centerx, event.pos[1] - dogRect.centery)

        if not reverseCheat and not slowCheat:
            monsterAddCounter += 1
        if monsterAddCounter == ADDNEWMONSTERRATE:
            monsterAddCounter = 0
            monsterSize = random.randint(MONSTERINSIZE, MONSTERMAXSIZE)
            newMonster = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-monsterSize), 0 - monsterSize,monsterSize, monsterSize),
                        'speed': random.randint(MONSTERMINSPEED, MONSTERMAXSPEED),
                        'surface':pygame.transform.scale(monsterImage, (monsterSize, monsterSize)),
                        }

            monsters.append(newMonster)

        if moveLeft and dogRect.left > 0:
            dogRect.move_ip(-1 * DOGMOVERATE, 0)
        if moveRight and dogRect.right < WINDOWWIDTH:
            dogRect.move_ip(DOGMOVERATE, 0)
        if moveUp and dogRect.top > 0:
            dogRect.move_ip(0, -1 * DOGMOVERATE)
        if moveDown and dogRect.bottom < WINDOWHEIGHT:
            dogRect.move_ip(0, DOGMOVERATE)

        pygame.mouse.set_pos(dogRect.centerx, dogRect.centery)

        for b in monsters:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in monsters[:]:
            if b['rect'].top > WINDOWHEIGHT:
                monsters.remove(b)

        windowSurface.fill(BACKGROUNDCOLOR)

        drawText('Оцінка : %s' % (score), font, windowSurface, 10, 0)
        drawText('Найвища оцінка: %s' % (topScore), font, windowSurface, 10, 40)

        windowSurface.blit(dogImage, dogRect)

        for b in monsters:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if dogHasHitMonster(dogRect, monsters):
            if score > topScore:
                topScore = score 
            break

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('Гра закінчена', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Натисніть щоб зіграти знову.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForDogToPressKey()

    gameOverSound.stop()
