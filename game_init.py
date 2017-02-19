import pygame
from pygame.locals import *
from sprites import *
from assets import *

def game_init(player):
    player = Player(player_img_name, 10, 5, 100, 100)
