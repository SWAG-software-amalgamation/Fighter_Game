import pygame
import random
from time import sleep
from screeninfo import get_monitors
import time
from os import startfile
import sys

# 게임에 사용되는 전역 변수 정의
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (20,250,250)
width, height = int(str(get_monitors()[0]).split(',')[2].split('=')[1]), int(str(get_monitors()[0]).split(',')[3].split('=')[1])
start_width = int(width/3)
pad_width = start_width*2
pad_height = height
fight_width = 36
fight_height = 38
enemy_width = 26
enemy_height = 20
isHack = False
shotcount = 0
kaist_e_c_check = []
kaist_e_c_on_check = 0

def score_update(N):
    M = list(map(int, open("./score.txt", 'r').readlines() + [f'{N}\n']))
    M.sort()
    M.reverse()
    M = list(map(str, M))
    open('./score.txt','w').write('\n'.join(M[:-1]))

def gameover():
    global gamepad, isHack, kaist_e_c_on_check
    if kaist_e_c_on_check == 0:
        isHack = False
        dispMessage('Game Over')
    else:
        open("./Kaist Egg/kaist_e_c_c_check.txt",'w').write(str(time.time()))
        dispMessage('Clear')

# 적을 맞춘 개수 계산
def drawScore(count):
    global gamepad, shotcount, kaist_e_c_on_check
    shotcount = count
    font = pygame.font.Font('neodgm.ttf', 30)
    if kaist_e_c_on_check == 0:
        text = font.render('Enemy Kills: ' + str(count), True, WHITE)
    else:
        text = font.render(f'Enemy Kills: {count}/20', True, WHITE)
    gamepad.blit(text, (10, 0))

def drawPassed(count):
    global gamepad

    font = pygame.font.Font('neodgm.ttf', 30)
    text = font.render(f'Enemy Passed: {count}/3', True, RED)
    gamepad.blit(text, (280, 0))
    font = pygame.font.Font('neodgm.ttf', 23)
    text = font.render(', '.join(list(map(str,[0, 1, 2, 3, 2, 3, 0, 1, 4, 5, 6, 7, 4, 8, 4, 9, 9]))), True, RED)
    gamepad.blit(text, (10, 40))


# 화면에 글씨 보이게 하기
def dispMessage(text):
    global gamepad, shotcount, kaist_e_c_on_check

    textfont = pygame.font.Font('neodgm.ttf', 100)
    text = textfont.render(text, True, RED)    
    textpos = text.get_rect()
    textpos.center = ((width)/2, pad_height/2-60)
    gamepad.blit(text, textpos)
    if kaist_e_c_on_check == 0:
        sctextfont = pygame.font.Font('neodgm.ttf', 50)
        if shotcount - 10 < 0:
            sctext = sctextfont.render('SCORE: 0'+str(shotcount), True, YELLOW)
        else:
            sctext = sctextfont.render('SCORE: '+str(shotcount), True, YELLOW)
        sctextpos = text.get_rect()
        sctextpos.center = ((width)/2+(width/8), pad_height/2+50)
        gamepad.blit(sctext, sctextpos)
    
    pygame.display.update()
    score_update(shotcount)
    sleep(3)
    startfile('read_leaderboard_pyqt.py')
    pygame.quit()
    sys.exit()


def crash(): 
    global gamepad, isHack
    isHack = False
    dispMessage('GAME OVER!')
    

# 게임에 등장하는 객체를 그려줌
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))

# 게임 실행 메인 함수
def runGame():
    global gamepad, fighter, clock, isHack
    global bullet, enemy
    global kaist_e_c_check, kaist_e_c_on_check

    isShot = False
    shotcount = 0
    enemypassed = 0

    x = pad_width*0.45
    y = pad_height*0.9
    x_change = 0

    bullet_xy = []
    enemy_x = random.randrange(start_width+enemy_width, pad_width-enemy_width)
    enemy_y = 0
    enemy_speed = 5
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (int(pad_width/2), pad_height))
        
    ongame = False
    while not ongame:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                ongame = True

            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if event.key == pygame.K_LEFT:
                    x_change -= 5
                    if len(kaist_e_c_check) == 0 or kaist_e_c_check == [0,1,2,3,2,3]:
                        kaist_e_c_check.append(0)
                    else:
                        kaist_e_c_check = []
                    
                elif event.key == pygame.K_RIGHT:
                    x_change += 5
                    if kaist_e_c_check == [0] or kaist_e_c_check == [0,1,2,3,2,3,0]:
                        kaist_e_c_check.append(1)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_UP:
                    if kaist_e_c_check == [0, 1] or kaist_e_c_check == [0,1,2,3]:
                        kaist_e_c_check.append(2)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_DOWN:
                    if kaist_e_c_check == [0, 1, 2] or kaist_e_c_check == [0,1,2,3,2]:
                        kaist_e_c_check.append(3)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_e :
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1] or kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6,7] or kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6,7,4,8]:
                        kaist_e_c_check.append(4)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_a:
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1,4]:
                        kaist_e_c_check.append(5)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_s:
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5]:
                        kaist_e_c_check.append(6)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_t:
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6]:
                        kaist_e_c_check.append(7)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_r:
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6,7,4]:
                        kaist_e_c_check.append(8)
                    else:
                        kaist_e_c_check = []
                elif event.key == pygame.K_g:
                    if kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6,7,4,8,4]:
                        kaist_e_c_check.append(9)
                    elif kaist_e_c_check == [0,1,2,3,2,3,0,1,4,5,6,7,4,8,4,9]:
                        kaist_e_c_check.append(9)
                        kaist_e_c_on_check = 1
                        background_image = pygame.image.load('./Kaist Egg/background.jpg')
                        background_image = pygame.transform.scale(background_image, (int(pad_width/2), pad_height))
                        shotcount = 0
                    else:
                        kaist_e_c_check = []
                       
                elif event.key == pygame.K_SPACE:
                    if len(bullet_xy) < 2*3:    # 한번에 3개까지 발사
                        bullet_x = x + fight_width/2 - 5
                        bullet_y = y - fight_height
                        bullet_xy.append([bullet_x, bullet_y])
                        
                        bullet_x = x + fight_width/2 + 5
                        bullet_y = y - fight_height
                        bullet_xy.append([bullet_x, bullet_y])

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        print(kaist_e_c_check)

        gamepad.fill(BLACK)
        gamepad.blit(background_image, (start_width, 0))

        x += x_change
        if x < start_width+enemy_width:
            x = pad_width - fight_width
        elif x > pad_width - fight_width:
            x = start_width+enemy_width

       # 게이머 전투기가 적과 충돌했는지 체크
        if y < enemy_y + enemy_height:
            if (enemy_x > x and enemy_x < x + fight_width) or \
               (enemy_x + enemy_width > x and enemy_x+ enemy_width < x + fight_width):
                crash()

        drawObject(fighter, x, y)
        

       # 전투기 무기 발사 구현
        if len(bullet_xy) != 0:
            for i, bxy in enumerate(bullet_xy):
                bxy[1] -= 5
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y:
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width:
                        bullet_xy.remove(bxy)
                        isShot = True

                        shotcount += 1
                
                if bxy[1] <= 0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        drawScore(shotcount)


        # 적 구현
        enemy_y += enemy_speed    

        if enemy_y > pad_height:
            enemy_x = random.randrange(start_width+enemy_width, pad_width-enemy_width)
            enemy_y = 0
            enemypassed += 1

        if enemypassed == 3:
            gameover()

        drawPassed(enemypassed)
        
        if isShot:
            enemy_speed += 1
            if enemy_speed >= 8:
                enemy_speed = 8
                
            enemy_x = random.randrange(start_width+enemy_width, pad_width-enemy_width)
            enemy_y = 0                      
            isShot = False

        if shotcount >= 20:
            gameover()

        if kaist_e_c_on_check == 0:
            drawObject(enemy, enemy_x, enemy_y)
        else:
            drawObject(kaist_e, enemy_x, enemy_y)
                
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def initGame():
    global gamepad, fighter, clock
    global bullet, enemy, kaist_e

    pygame.init()
    gamepad = pygame.display.set_mode((width, height))
    pygame.display.set_caption('전투기게임')
    fighter = pygame.image.load('fighter.png')
    enemy = pygame.image.load('enemy.png')
    bullet = pygame.image.load('bullet.png')
    kaist_e = pygame.image.load('./Kaist Egg/non_break (1).png')
    isHack = False
    clock = pygame.time.Clock()   

try:
    initGame()
    runGame()
except:
    pygame.quit()
