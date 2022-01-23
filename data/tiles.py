import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, collidable):
        pygame.sprite.Sprite.__init__(self)
        # may need to add more images if i want animated tiles; or make a new class for them
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        self.collidable = collidable
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Tilemap():
    def __init__(self, filename):
        self.tile_size = 64
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        # no opacity or black color 
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0,0))
    # load map function
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)
            # may have to change if i want animating tiles
    
    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    # load tiles function
    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0,0
        for row in map:
            x = 0
            for tile in row:
                # add tiles when necessary
                if tile == '0':
                    tiles.append(Tile('data/assets/ground.png', x * self.tile_size, y * self.tile_size, False))
                elif tile == '1':
                    tiles.append(Tile('data/assets/water.png', x * self.tile_size, y * self.tile_size, True))
                elif tile == '2':
                    tiles.append(Tile('data/assets/water2.png', x * self.tile_size, y * self.tile_size, True))
                x += 1
            y += 1
        
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles