from genericpath import getmtime
import pygame
from pygame.constants import KEYDOWN, KEYUP, K_e

from tiles import *
from player import Player
from check_input import *
from objects import *

pygame.init()
clock = pygame.time.Clock()

WIN_SIZE = (640, 640)
target_fps = 60

pygame.display.set_caption("Evolution")
screen = pygame.display.set_mode(WIN_SIZE, 0, 32)
player = Player()

map = Tilemap('assets/map.csv')
objMap = ObjectMap('assets/objMap.csv')
running = True
gameFont = pygame.font.SysFont("Andale Mono", 20)

# change map and sprites to make an island with animations

while running:
    # delta time
    dt = clock.tick(60) * .001 * target_fps

    # get input for interaction; maybe change and put in check_input.py
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_e:
                player.E_KEY = True
        if event.type == KEYUP:
            if event.key == K_e:
                player.E_KEY = False                                          # check input
        player.LEFT_KEY, player.RIGHT_KEY, player.DOWN_KEY, player.UP_KEY =  check(event, player.LEFT_KEY, player.RIGHT_KEY, player.UP_KEY, player.DOWN_KEY)
    objMap.update()
    player.update(dt, map.tiles, objMap.objs)
    # plant count text
    textSurf = gameFont.render(str(player.plantCount),False, (255,255,255))
    # clear screen
    screen.fill((0, 255, 255))
    # draw map first
    map.draw_map(screen)
    # draw objects second
    objMap.draw_map(screen)
    # draw player last
    player.draw(screen)
    # add the text for the plant count
    screen.blit(textSurf, (20, 20))
    # update the display
    pygame.display.update()