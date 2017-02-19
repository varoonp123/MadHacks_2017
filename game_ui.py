import pygame
from pygame.locals import *
from assets import *

def display_health(screen,health):
    offset = 50
    loc = [10, 10]
    full_hearts = int(health/2)
    half_hearts = health%2

    print('Full hearts: ' + str(full_hearts) + ' Half hearts: ' + str(half_hearts))

    for _ in range (0, full_hearts):
        screen.blit(pygame.image.load(full_heart_img), loc)
        loc[0] += offset

    for _ in range (0, half_hearts):
        screen.blit(pygame.image.load(half_heart_img), loc)
        loc[0] += offset
    
    
