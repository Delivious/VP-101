import pygame 
import time
import os
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
bullets = []
shotWaitTime = 500
recentShot = 0

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
    if keys[pygame.K_SPACE] and (((time.time()) * 1000) - recentShot) > shotWaitTime:
            bullets.append([x, screen_height - 150])
            recentShot = (time.time()) * 1000
    screen.fill((0,0,0))
    if (screen_width/2 - 35) + player.x <= 0:
        x = 0
    elif (screen_width/2 - 35) + player.x >= screen_width - 100:
        x = screen_width - 100
    else:
        x = (screen_width/2 - 35) + player.x
    screen.blit(player.image, (x, (screen_height - 150)))
    for bullet in bullets:
        updBullet(bullet)
    pygame.display.update()

    clock.tick(60)

pygame.quit() 
quit() 