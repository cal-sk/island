from json import load
import pygame, csv, os, time


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, x, y, collidable):
        pygame.sprite.Sprite.__init__(self)
        # building variables
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.collidable = collidable
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
            
class BuildMap():
    # init function
    def __init__(self, filename):
        self.tile_size = 64
        self.builds = self.load_obj(filename) 
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_alpha(180)
        self.load_map()
    # draw map on screen surface in main.py
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    def update(self):
        for build in self.builds:
            build.update() # update the builds when destroyed
        self.load_map() # then load the map
    # load map
    def load_map(self):
        # CLEAR PREVIOUS MAP SO IT DOESNT LAYER
        self.map_surface.fill((0,0,0,0))
        # iterate through builds and draw them
        for build in self.builds:
            build.draw(self.map_surface)
    # read csv for map
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    # loading build
    def load_build(self, filename):
        builds = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for build in row:
                # add more builds as necessary
                if build == '1': 
                    builds.append(Wall('data/assets/coin.png', x * self.tile_size, y * self.tile_size, True))
                x += 1
            y += 1
        
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return builds