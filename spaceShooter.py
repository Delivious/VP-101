import random
import pygame 
import time
import os
import threading
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init() 

screen_width=1080 
screen_height=720 

GREEN = (0, 255, 0)

powerGreen = pygame.image.load('Assets/PNG/Power-ups/powerupGreen_star.png')
powerBlue = pygame.image.load('Assets/PNG/Power-ups/powerupBlue_star.png')
powerRed = pygame.image.load('Assets/PNG/Power-ups/powerupRed_star.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
      super().__init__()
      self.image = pygame.image.load('Assets/PNG/playerShip1_blue.png')
      self.x = 0
      self.y = 0
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
    def mode(self, selectedMode):
        if selectedMode == 1:
            self.image1 = pygame.image.load('Assets/Enemies/enemyGreen1.png')
        elif selectedMode == 2:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlue1.png')
        elif selectedMode == 3:
            self.image1 = pygame.image.load('Assets/Enemies/enemyRed1.png')
        else:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlack1.png')
    def update(self):
        self.y+=0.5
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
    def update(self):
        self.y += 1
def updShips(enemies):
    for enemy in enemies:
        enemy.update()

def spawnEnemies():
    global enemies
    enemiesSpawn = 9
    while True:
        enemiesSpawn+=1
        time.sleep(5)
        randMode = random.randint(1, 4)
        for i in range(enemiesSpawn):
            enemy = Enemy()
            enemy.mode(randMode)
            enemy.x = random.randint(50, screen_width - 100)
            enemy.y = random.randint(-200, -100)
            enemies.append(enemy)

def despawnWreckFunc(wreck):
    global wreckage
    time.sleep(1)
    if wreck in wreckage:
        wreckage.remove(wreck)

def resetPowerupTimer():
    global powerTimer

    try:
        if powerTimer.is_alive():
            powerTimer.cancel()
    except:
        pass

    powerTimer = threading.Timer(15, powerupTimer)
    powerTimer.start()

def powerupTimer():
    global powerup
    powerup = 1
    resetPowerupTimer()

def powerUpCollision():
    global powerups, powerup, powerTimer
    for power in powerups:
        if power.x > x and power.x < x + player.image.get_width() and power.y > y and power.y < y + player.image.get_height():
            powerImage = power.image
            powerups.remove(power)
            if powerImage == powerGreen:
                powerup = 1
                resetPowerupTimer()
            if powerImage == powerBlue:
                powerup = 3
            if powerImage == powerRed:
                powerup = 2
                resetPowerupTimer()

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
                if bullet_rect.colliderect(enemy_rect):
                    enemiesToRemove.append(enemy)
                    pygame.mixer.Sound('Assets/Bonus/explosion.mp3').play()
                    randomPowerup = random.randint(1,150)
                    if randomPowerup == 50:
                        power = PowerUp(powerGreen, enemy.x, enemy.y)
                    elif randomPowerup == 100:
                        power = PowerUp(powerBlue, enemy.x, enemy.y)
                    elif randomPowerup == 150:
                        power = PowerUp(powerRed, enemy.x, enemy.y)
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

screen = pygame.display.set_mode((screen_width, screen_height)) 

pygame.display.set_caption("Space Shooter") 

screen.fill((0, 0, 0))


clock = pygame.time.Clock() 
pygame.mixer.Sound('Assets/Bonus/music.mp3').play(loops=99999999)
powerup = 1
keep_playing=True 
bullet_image1 = pygame.image.load('Assets/PNG/Lasers/laserBlue14.png')
bullet_image2 = pygame.image.load('Assets/PNG/Lasers/laserRed08.png')
bullet_image3 = pygame.image.load('Assets/PNG/Lasers/laserGreen11.png')
player = Player()
x = (screen_width/2 - 35) + player.x
y = (screen_height - 150) + player.y
wreckage = []
powerups = []
bullets = []
enemies = []
shotWaitTime = 400
recentShot = 0
enemySpawnThread = threading.Thread(target=spawnEnemies, daemon=True)
enemySpawnThread.start()
screen.blit(player.image, (screen_width/2 - 35, screen_height - 150))
while keep_playing==True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            keep_playing = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if x < screen_width - 100:  
            player.x+=5
        else:
            player.x-=1
    if keys[pygame.K_a]:
        if x > 0:     
            player.x-=5
        else:
            player.x+=1
    if keys[pygame.K_w]:
        if y > 0:
            player.y -= 5
        else:
            player.y += 1
    if keys[pygame.K_s]:
        if y < screen_height - 100:
            player.y += 5
        else:
            player.y -= 1
    if keys[pygame.K_SPACE] and (((time.time()) * 1000) - recentShot) > shotWaitTime:
            if powerup == 3:
                pierces = 3
                bullets.append([x + 42, screen_height - 200 + player.y, bullet_image1, pierces])
                shotWaitTime = 400
            elif powerup == 2:
                shotWaitTime = 650
                pierces = 1
                bullets.append([x + 42, screen_height - 200 + player.y, bullet_image2, pierces])
                bullets.append([x - 22, screen_height - 200 + player.y, bullet_image2, pierces])
                bullets.append([x + 102, screen_height - 200 + player.y, bullet_image2, pierces])
            elif powerup == 1:
                pierces = 1
                shotWaitTime = 250
                bullets.append([x + 42, screen_height - 200 + player.y, bullet_image3, pierces])
            recentShot = (time.time()) * 1000
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
    pygame.display.update()
   

    clock.tick(60)

pygame.quit() 
quit() 