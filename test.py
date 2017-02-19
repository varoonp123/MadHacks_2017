
import pygame
from pygame.locals import *
from sys import exit
from sprites import *
import random as rand
from rooms import *

clock = pygame.time.Clock()
fps = 60



pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE,0,32)

test_room = Room(1,2)

print(test_room)
test_room.generate(screen)


while True:
    dt = clock.tick(fps)
    speed = float(dt)/64



    '''
    for e in test_room.enemies:
        e.behave(speed)
    '''
    print(test_room.enemies)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    pygame.display.update()
