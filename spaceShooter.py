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
            self.image2 = pygame.image.load('Assets/Enemies/enemyGreen2.png')
            self.image3 = pygame.image.load('Assets/Enemies/enemyGreen3.png')
            self.image4 = pygame.image.load('Assets/Enemies/enemyGreen4.png')
            self.image5 = pygame.image.load('Assets/Enemies/enemyGreen5.png')
        elif selectedMode == 2:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlue1.png')
            self.image2 = pygame.image.load('Assets/Enemies/enemyBlue2.png')
            self.image3 = pygame.image.load('Assets/Enemies/enemyBlue3.png')
            self.image4 = pygame.image.load('Assets/Enemies/enemyBlue4.png')
            self.image5 = pygame.image.load('Assets/Enemies/enemyBlue5.png')
        elif selectedMode == 3:
            self.image1 = pygame.image.load('Assets/Enemies/enemyRed1.png')
            self.image2 = pygame.image.load('Assets/Enemies/enemyRed2.png')
            self.image3 = pygame.image.load('Assets/Enemies/enemyRed3.png')
            self.image4 = pygame.image.load('Assets/Enemies/enemyRed4.png')
            self.image5 = pygame.image.load('Assets/Enemies/enemyRed5.png')
        else:
            self.image1 = pygame.image.load('Assets/Enemies/enemyBlack1.png')
            self.image2 = pygame.image.load('Assets/Enemies/enemyBlack2.png')
            self.image3 = pygame.image.load('Assets/Enemies/enemyBlack3.png')
            self.image4 = pygame.image.load('Assets/Enemies/enemyBlack4.png')
            self.image5 = pygame.image.load('Assets/Enemies/enemyBlack5.png')
    def update(self):
        self.y+=0.5
def updShips(enemies):
    for enemy in enemies:
        enemy.update()

def spawnEnemies():
    global enemies
    enemiesSpawn = 9
    while True:
        enemiesSpawn+=1
        xPos = 50
        yPos = 50
        time.sleep(5)
        randMode = random.randint(1, 4)
        for i in range(enemiesSpawn):
            if xPos > screen_width - 100:
                yPos += 50
                xPos = 50
            enemy = Enemy()
            enemy.mode(randMode)
            enemy.x = xPos
            enemy.y = yPos
            enemies.append(enemy)
            xPos += 100

def updBullet(bullet):
    bullet[1] -= 5
    if bullet[1] < 0:
        bullets.remove(bullet)
    else:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

screen = pygame.display.set_mode((screen_width, screen_height)) 

pygame.display.set_caption("Space Shooter") 

screen.fill((0, 0, 0))


clock = pygame.time.Clock() 


keep_playing=True 
bullet_image = pygame.image.load('Assets/PNG/Lasers/laserBlue14.png')
player = Player()
x = (screen_width/2 - 35) + player.x
y = (screen_height - 150) + player.y
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
            bullets.append([x + 42, screen_height - 200])
            recentShot = (time.time()) * 1000
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
    for bullet in bullets:
        updBullet(bullet)
    for enemy in enemies:
        screen.blit(enemy.image1, (enemy.x, enemy.y))
    updShips(enemies)
    pygame.display.update()

    clock.tick(60)

pygame.quit() 
quit() 