from json import load
import pygame, csv, os, time


class PlantObject(pygame.sprite.Sprite):
    # init function
    def __init__(self,image1, image2, image3, image4, x, y, interact, xsize, ysize):
        pygame.sprite.Sprite.__init__(self)
        # image sprites
        self.image1 = pygame.image.load(image1)
        self.image1 = pygame.transform.scale(self.image1, (64, 64))
        self.image2 = pygame.image.load(image2)
        self.image2 = pygame.transform.scale(self.image2, (64, 64))
        self.image3 = pygame.image.load(image3)
        self.image3 = pygame.transform.scale(self.image3, (64, 64))        
        self.image4 = pygame.image.load(image4)
        self.image4 = pygame.transform.scale(self.image4, (64, 64))
        self.current_image = self.image1
        # set rect equal to given rect size
        self.rect = pygame.Rect(x, y, xsize, ysize)
        self.interactable = interact
        self.max = 3
        self.stock = self.max
        self.timer = 0
    # update function
    def update(self):
        if self.stock < self.max:
            self.time()
            if self.timer == 300: # 5 seconds
                self.stock += 1
                self.timer = 0
        if self.stock == 3:
            self.current_image = self.image1
        if self.stock == 2:
            self.current_image = self.image2
        if self.stock == 1:
            self.current_image = self.image3
        if self.stock == 0:
            self.current_image = self.image4
    # time function for plant regrowth
    def time(self):
        self.timer += 1
    # draw function
    def draw(self, surface): 
        surface.blit(self.current_image, (self.rect.x, self.rect.y))
    # interact function called by player.py
    def interact(self):
        self.stock -= 1
        # func gets called by player
       
            
class ObjectMap():
    # init function
    def __init__(self, filename):
        self.tile_size = 64
        self.objs = self.load_obj(filename) 
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_alpha(180)
        self.load_map()
    # draw map on screen surface in main.py
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    def update(self):
        for obj in self.objs:
            obj.update() # update the objects current_image
        self.load_map() # then load the map
    # load map
    def load_map(self):
        # CLEAR PREVIOUS MAP SO IT DOESNT LAYER
        self.map_surface.fill((0,0,0,0))
        # iterate through objects and draw them
        for obj in self.objs:
            obj.draw(self.map_surface)
    # read csv for map
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    # loading objects
    def load_obj(self, filename):
        objs = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for obj in row:
                # add more objs as necessary
                if obj == '1': 
                    objs.append(PlantObject('assets/coin.png', 'assets/coin2.png','assets/coin3.png','assets/coin4.png', x * self.tile_size, y * self.tile_size, True,64, 64))
                x += 1
            y += 1
        
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return objs