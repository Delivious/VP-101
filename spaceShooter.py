import random
try:
    import pygame
except ModuleNotFoundError:
    print("Must have pygame installed to run game.") 
import time
import os
import threading
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init() 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen_width, screen_height = pygame.display.get_surface().get_size()

GREEN = (0, 255, 0)

powerGreen = pygame.image.load('Assets/PNG/Power-ups/powerupGreen_star.png')
powerBlue = pygame.image.load('Assets/PNG/Power-ups/powerupBlue_star.png')
powerRed = pygame.image.load('Assets/PNG/Power-ups/powerupRed_star.png')

font = pygame.font.Font(None, 50)



class Player(pygame.sprite.Sprite):
    def __init__(self):
      super().__init__()
      self.image = pygame.image.load('Assets/PNG/playerShip1_blue.png')
      self.x = 0
      self.y = 0
      self.score = 0
    def addScore(self, increase):
        self.score+=increase
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.increase = 0.5
        self.points = 0
        self.health = 0
        self.bulletids = []
    def mode(self, selectedMode):
        if selectedMode == 1:
            self.image1 = pygame.image.load('Assets/Enemies/enemyGreen1.png')
            self.health = 1
            self.points = 1
        elif selectedMode == 2:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlue1.png')
            self.health = 2
            self.points = 2
        elif selectedMode == 3:
            self.image1 = pygame.image.load('Assets/Enemies/enemyRed1.png')
            self.health = 3
            self.points = 3
        else:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlack1.png')
            self.health = 4
            self.points = 4
    def update(self):
        self.y+=self.increase
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, x, y, name):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.name = name
    def update(self):
        self.y += 1
def updShips(enemies):
    for enemy in enemies:
        enemy.update()

def spawnEnemies():
    global enemies
    enemiesSpawn = 9
    while True:
        if enemiesSpawn > 10:
            enemySpeed=0.5
        else:    
            enemiesSpawn+=1
        time.sleep(5)
        randMode = random.randint(1, 4)
        for i in range(enemiesSpawn):
            enemy = Enemy()
            enemy.mode(randMode)
            enemy.x = random.randint(50, screen_width - 100)
            enemy.y = random.randint(-200, -100)
            try:
                if enemiesSpawn > 25:
                    enemy.increase += enemySpeed
            except:
                pass
            enemies.append(enemy)

def despawnWreckFunc(wreck):
    global wreckage
    time.sleep(1)
    if wreck in wreckage:
        wreckage.remove(wreck)

def resetPowerupTimer(powerToReset):
    global shotPowerTimer, piercePowerTimer

    if powerToReset == 'red':
        try:
            shotPowerTimer.cancel()
        except:
            pass

        shotPowerTimer = threading.Timer(15, shotPowerupTimer)
        shotPowerTimer.start()

    elif powerToReset == 'blue':
        try:
            piercePowerTimer.cancel()
        except:
            pass

        piercePowerTimer = threading.Timer(15, piercePowerupTimer)
        piercePowerTimer.start()
    

def shotPowerupTimer():
    global ifGreen, ifShotgun, ifPierce, activePowers
    ifShotgun[1] = False
def piercePowerupTimer():
    global ifGreen, ifShotgun, ifPierce, activePowers
    ifPierce[1] = False

def powerUpCollision():
    global powerups, ifGreen, powerTimer, ifPierce, ifShotgun
    for power in powerups:
        if power.x > x and power.x < x + player.image.get_width() and power.y > y and power.y < y + player.image.get_height():
            powerImage = power.image
            powerups.remove(power)
            if powerImage == powerBlue:
                ifPierce[1] = True
                activePowers.append(ifPierce)
                resetPowerupTimer(ifPierce[0])
            if powerImage == powerRed:
                ifShotgun[1] = True
                activePowers.append(ifShotgun)
                resetPowerupTimer(ifShotgun[0])
def shipEnemyCollision():
    global gameOver, x, y
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image1.get_width(), enemy.image1.get_height())
        player_rect = pygame.Rect(x, y, player.image.get_width(), player.image.get_height())
        if enemy_rect.colliderect(player_rect):
            gameOver = True
        if enemy.y >= screen_height:
            gameOver = True
def detectCollision():
    global wreckage, powerups
    bulletsToRemove = []
    enemiesToRemove = []
    for bullet in bullets:
        if bullet in bulletsToRemove:
            continue
        if bullet[3] > 0:
            for enemy in enemies:
                if enemy in enemiesToRemove:
                    continue
                bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet[2].get_width(), bullet[2].get_height())
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image1.get_width(), enemy.image1.get_height())
                if bullet_rect.colliderect(enemy_rect) and bullet[5] not in enemy.bulletids:
                    enemy.health-=bullet[4]
                    enemy.bulletids.append(bullet[5])
                    if enemy.health <= 0:
                        player.addScore(enemy.points)
                        enemiesToRemove.append(enemy)
                        pygame.mixer.Sound('Assets/Bonus/explosion.mp3').play()
                        randomPowerup = random.randint(1,100)
                        if randomPowerup == 66:
                            power = PowerUp(powerBlue, enemy.x, enemy.y, 'blue')
                        elif randomPowerup == 99:
                            power = PowerUp(powerRed, enemy.x, enemy.y, 'red')
                        try:
                            if power:
                                powerups.append(power)
                        except Exception as e:
                            pass
                    bullet[3] -= 1
        if bullet[3] <= 0:
            bulletsToRemove.append(bullet)
    for bullet in bulletsToRemove:
        try:
            bullets.remove(bullet)
        except ValueError:
            continue
    for enemy in enemiesToRemove:
        try:
            enemies.remove(enemy)
        except ValueError:
            continue

def updBullet(bullet):
    bullet[1] -= 5
    if bullet[1] < -100:
        return True
    else:
        screen.blit(bullet[2], (bullet[0], bullet[1]))
        return False
def typeUsername():
    screen.fill((0, 0, 0))
    usernameTyping = True
    username = []
    curTime = time.time() * 1000
    waittime = 50

    while usernameTyping:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                elapsed = (time.time() * 1000) - curTime
                if elapsed >= waittime:
                    if event.key == pygame.K_BACKSPACE:
                        if username:
                            username.pop()
                            curTime = time.time() * 1000
                    elif event.key == pygame.K_RETURN:
                        usernameTyping = False
                    else:
                        char_pressed = event.unicode
                        if char_pressed and char_pressed.isprintable():
                            username.append(char_pressed)
                            curTime = time.time() * 1000

        word = ''.join(username)
        screen.fill((0, 0, 0))
        usernamePrompt = font.render('Type Your Username:', True, (255, 255, 255))
        usernameInput = font.render(word, True, (255, 255, 255))
        screen.blit(usernamePrompt, (screen_width/2, 300))
        screen.blit(usernameInput, (screen_width/2, 500))
        pygame.display.update()

    return ''.join(username)


def typePassword():
    screen.fill((0, 0, 0))
    passwordTyping = True
    password = []
    curTime = time.time() * 1000
    waittime = 50

    while passwordTyping:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                elapsed = (time.time() * 1000) - curTime
                if elapsed >= waittime:
                    if event.key == pygame.K_BACKSPACE:
                        if password:
                            password.pop()
                            curTime = time.time() * 1000
                    elif event.key == pygame.K_RETURN:
                        passwordTyping = False
                    else:
                        char_pressed = event.unicode
                        if char_pressed and char_pressed.isprintable():
                            password.append(char_pressed)
                            curTime = time.time() * 1000

        masked = '*' * len(password)
        screen.fill((0, 0, 0))
        passwordPrompt = font.render('Type Your Password:', True, (255, 255, 255))
        passwordInput = font.render(masked, True, (255, 255, 255))
        screen.blit(passwordPrompt, (screen_width/2, 300))
        screen.blit(passwordInput, (screen_width/2, 500))
        pygame.display.update()

    return ''.join(password)


def makeAccount():
    username = typeUsername()
    password = typePassword()
    return username, password


screen = pygame.display.set_mode((screen_width, screen_height)) 

pygame.display.set_caption("Space Shooter") 
def game():
    screen.fill((0, 0, 0))
    global gameOverScreen, ifGreen, ifPierce, ifShotgun, keep_playing, gameOver, bullet_image1, bullet_image2, bullet_image3, player, x, y, wreckage, activePowers, bullets, powerups, enemies, bulletid, keys, clock, gameOver
    clock = pygame.time.Clock() 
    music = pygame.mixer.Sound('Assets/Bonus/music.mp3')
    music.play(loops=10)
    ifGreen = ['green', True]
    ifPierce = ['blue', False]
    ifShotgun = ['red', False]
    keep_playing=True 
    gameOver = False
    bullet_image1 = pygame.image.load('Assets/PNG/Lasers/laserBlue14.png')
    bullet_image2 = pygame.image.load('Assets/PNG/Lasers/laserRed08.png')
    bullet_image3 = pygame.image.load('Assets/PNG/Lasers/laserGreen11.png')
    player = Player()
    x = (screen_width/2 - 35) + player.x
    y = (screen_height - 150) + player.y
    wreckage = []
    activePowers = []
    powerups = []
    bullets = []
    enemies = []
    bulletid=1
    shotWaitTime = 650
    greenWaitTime = 250
    recentShotGreen = (time.time()) * 1000
    recentShotPierce = (time.time()) * 1000
    pierceWaitTime = 400
    recentShot = 0
    enemySpawnThread = threading.Thread(target=spawnEnemies, daemon=True)
    enemySpawnThread.start()
    score = font.render(f'Score: {player.score}', True, (255,255,255))
    screen.blit(player.image, (screen_width/2 - 35, screen_height - 150))
    while keep_playing==True: 
        keys = pygame.key.get_pressed()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]: 
                keep_playing = False
        
        if keys[pygame.K_d]:
            if x < screen_width - 100:  
                player.x+=8
            else:
                player.x-=1
        if keys[pygame.K_a]:
            if x > 0:     
                player.x-=8
            else:
                player.x+=1
        if keys[pygame.K_w]:
            if y > 0:
                player.y -= 8
            else:
                player.y += 1
        if keys[pygame.K_s]:
            if y < screen_height - 100:
                player.y += 8
            else:
                player.y -= 1
        if keys[pygame.K_SPACE]:
                if ifPierce[1] and (((time.time()) * 1000) - recentShotPierce) > pierceWaitTime :
                    bulletid+=1
                    pierces = 3
                    damage = 2
                    bullets.append([x + 42, screen_height - 200 + player.y, bullet_image1, pierces, damage, bulletid])
                    pierceWaitTime = 400
                    recentShotPierce = (time.time()) * 1000
                    pygame.mixer.Sound('Assets/Bonus/sfx_laser2.ogg').play()
                if ifShotgun[1] and (((time.time()) * 1000) - recentShot) > shotWaitTime:
                    bulletid+=3
                    shotWaitTime = 650
                    pierces = 1
                    damage = 2
                    bullets.append([x + 42, screen_height - 200 + player.y, bullet_image2, pierces, damage, bulletid])
                    bullets.append([x - 22, screen_height - 200 + player.y, bullet_image2, pierces, damage, bulletid+1])
                    bullets.append([x + 102, screen_height - 200 + player.y, bullet_image2, pierces, damage, bulletid+2])
                    recentShot = (time.time()) * 1000
                    pygame.mixer.Sound('Assets/Bonus/sfx_laser2.ogg').play()
                if ifGreen[1] and (((time.time()) * 1000) - recentShotGreen) > greenWaitTime:
                    bulletid+=1
                    pierces = 1
                    damage = 1
                    greenWaitTime = 250
                    bullets.append([x + 42, screen_height - 200 + player.y, bullet_image3, pierces, damage, bulletid])
                    recentShotGreen = (time.time()) * 1000
                    pygame.mixer.Sound('Assets/Bonus/sfx_laser2.ogg').play()
                
                
        screen.fill((0,0,0))
        if (screen_width/2 - 35) + player.x <= 0:
            x = 0
        elif (screen_width/2 - 35) + player.x >= screen_width - 100:
            x = screen_width - 100
        else:
            x = (screen_width/2 - 35) + player.x
        if (screen_height - 150) + player.y <= 0:
            y = 0
        elif (screen_height - 150) + player.y >= screen_height - 100:
            y = screen_height - 100
        else:
            y = (screen_height - 150) + player.y
        screen.blit(player.image, (x, y))
        bulletsToRemove = []
        for bullet in bullets:
            check = updBullet(bullet)
            if check:
                bulletsToRemove.append(bullet)
        for bullet in bulletsToRemove:
            bullets.remove(bullet) 
        for enemy in enemies:
            screen.blit(enemy.image1, (enemy.x, enemy.y))
        for wreck in wreckage:
            screen.blit(wreck[0], (wreck[1], wreck[2]))
        updShips(enemies)
        detectCollision()
        for power in powerups:
            power.update()
            screen.blit(power.image, (power.x, power.y))
        powerUpCollision()
        score = font.render(f'Score: {player.score}', True, (255,255,255))
        screen.blit(score, (screen_width/2, 50))
        shipEnemyCollision()
        if gameOver:
            gameOverScreen = False
            music.stop()
            break
        pygame.display.update()
game()
if gameOver:
    screen.fill((0,0,0))
    gameOverMsg = font.render(f'Game Over With A Score Of: {player.score}', True, (255, 0, 0))
    tryAgain = font.render('Try Again? (Press Space)', True, (255, 0, 0))
    uploadScore = font.render('Upload Your Score To Leaderboard? (Press Enter)', True, (255, 0, 0))
    tryAgainRect = tryAgain.get_rect()
    uploadRect = uploadScore.get_rect()
    gameOverScreen = False
    lastTime = time.time() * 1000
    while gameOverScreen != True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                gameOverScreen = True
            else:
                waitime = 2000
                elapsed = (time.time() * 1000) - lastTime
                if keys[pygame.K_SPACE] and elapsed >= waitime:
                    gameOverScreen = True
                    game()
                elif keys[pygame.K_RETURN]:
                    accountInfo = makeAccount()
                    print(accountInfo)
                    gameOverScreen = True

            screen.blit(gameOverMsg, (screen_width/2, 100))
            screen.blit(tryAgain, (screen_width/2, 300))
            screen.blit(uploadScore, (screen_width/2, 500))
        pygame.display.update()
    clock.tick(60)

pygame.quit() 
quit() 