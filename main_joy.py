import pygame
from pygame.locals import *
import random
import os
import time
import math
import copy

# player = os.path.join('ball2.png')
# ball = os.path.join('ball.bmp')
up = os.path.join('pictures/tank_up.png')
down = os.path.join('pictures/tank_down.png')
left = os.path.join('pictures/tank_left.png')
right = os.path.join('pictures/tank_right.png')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)




class Player(pygame.sprite.Sprite):

    # direct = [angle, speed]
    def __init__(self, x, y, dirvect, tanktype):
        super().__init__()
        self.tanktype = tanktype
        self.image = pygame.image.load(up)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dirvect = dirvect
        self.speed = self.dirvect[1]

    def calculate_newpos(self, rect, dirvect):
        (angle, speed) = dirvect
        (dx, dy) = (speed*math.cos(math.radians(angle)), speed*math.sin(math.radians(angle)))
        return rect.move(dx, dy)

    def update(self):
        new_pos = self.calculate_newpos(self.rect, self.dirvect)
        self.rect = new_pos

    def move_down(self):
            self.image = pygame.image.load(down)
            self.dirvect[0] = 90
            self.dirvect[1] = self.speed

    def move_up(self):
            self.image = pygame.image.load(up)
            self.dirvect[0] = -90
            self.dirvect[1] = self.speed

    def move_right(self):
            self.image = pygame.image.load(right)
            self.dirvect[0] = 0
            self.dirvect[1] = self.speed

    def move_left(self):
            self.image = pygame.image.load(left)
            self.dirvect[0] = 180
            self.dirvect[1] = self.speed


# direct = [angle, speed]
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dirvect, speed):
        super().__init__()
        self.dirvect = copy.deepcopy(dirvect)
        self.dirvect[1] = speed * 3
        self.image = pygame.Surface([5, 5])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def calculate_newpos(self, rect, dirvect):
        (angle, speed) = dirvect
        (dx, dy) = (speed*math.cos(math.radians(angle)), speed*math.sin(math.radians(angle)))
        return rect.move(dx, dy)

    def update(self):
        new_pos = self.calculate_newpos(self.rect, self.dirvect)
        self.rect = new_pos
        if self.rect.bottom > screen_height:
            self.kill()
        if self.rect.top < 0:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > screen_width:
            self.kill()



pygame.init()

screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

player = Player(10,10, [90, 7], 1)
player2 = Player(200,200, [90, 7], 2)
all_sprites_list.add(player,player2)
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
pygame.key.set_repeat(50,50)

score = 0

# joystick

try:
   pygame.joystick.init()
   joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
   joysticks[0].init()
   joysticks[1].init()
   player1_joystick = joysticks[0]
   player2_joystick = joysticks[1]
except IndexError:
   player1_joystick = None
   player2_joystick = None

"""while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.locals.JOYAXISMOTION:
            player1jx, player1jy = player1_joystick.get_axis(0), player1_joystick.get_axis(1)
            if player1jx < 0:
                print("left")
            if player1jx > 0:
                print("right")
            if player1jy < 0:
                print("up")
            if player1jy > 0:
                print("down")
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event)"""


while not done:
    # --- Event Processing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.move_down()
            if event.key == pygame.K_UP:
                player.move_up()
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()

            if event.key == pygame.K_s:
                player2.move_down()
            if event.key == pygame.K_w:
                player2.move_up()
            if event.key == pygame.K_a:
                player2.move_left()
            if event.key == pygame.K_d:
                player2.move_right()

            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x, player.rect.y, player.dirvect, player.speed)
                bullet2 = Bullet(player2.rect.x, player2.rect.y, player2.dirvect, player2.speed)
                bullet_list.add(bullet, bullet2)
                all_sprites_list.add(bullet, bullet2)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.dirvect[1] = 0

            if event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d:
                player2.dirvect[1] = 0

        if event.type == pygame.locals.JOYAXISMOTION:
            player1jx, player1jy = player1_joystick.get_axis(0), player1_joystick.get_axis(1)
            if player1jx < 0:
                player.move_left()
            if player1jx > 0:
                player.move_right()
            if player1jy < 0:
                player.move_up()
            if player1jy > 0:
                player.move_down()
            if player1jx == 0 and player1jy == 0:
                player.dirvect[1] = 0


        if event.type == pygame.locals.JOYAXISMOTION:
            player2jx, player2jy = player2_joystick.get_axis(0), player2_joystick.get_axis(1)
            if player2jx < 0:
                player2.move_left()
            if player2jx > 0:
                player2.move_right()
            if player2jy < 0:
                player2.move_up()
            if player2jy > 0:
                player2.move_down()
            if player2jx == 0 and player2jy == 0:
                player2.dirvect[1] = 0

        if event.type == pygame.JOYBUTTONDOWN:
            if player1_joystick.get_button(0):
                bullet = Bullet(player.rect.x, player.rect.y, player.dirvect, player.speed)
                bullet_list.add(bullet)
                all_sprites_list.add(bullet)

            if player2_joystick.get_button(0):
                bullet2 = Bullet(player2.rect.x, player2.rect.y, player2.dirvect, player2.speed)
                bullet_list.add(bullet2)
                all_sprites_list.add(bullet2)

    all_sprites_list.update()

    for bullet in bullet_list:
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    screen.fill(WHITE)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)

pygame.quit()
