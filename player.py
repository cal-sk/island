from os import truncate
import pygame
from tiles import *
from objects import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False, False, False
        self.E_KEY = False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.animating = False
        # sprites list
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load("assets/player.png"), (32, 32)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("assets/player2.png"), (32, 32)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("assets/player3.png"), (32, 32)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("assets/player4.png"), (32, 32)))
        # current image for animation
        self.current_image = 0
        # so it changes image
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(320-64,320-64), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,0)
        self.speed = 0.6
        self.animatable = True
        self.plantCount = 0
        self.interactable = False
        self.interType = None
    # add to the amount of plants
    def plantInteract(self):
        self.plantCount += 1

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
 
    # animation
    def anim_run(self):
        if self.animatable:
            self.animating = True
            self.current_image += 0.3 # this sets the speed of animation
            if self.current_image >= len(self.sprites):
                self.current_image = 1
            self.image = self.sprites[int(self.current_image)]
    # stop animation
    def anim_stop(self):
        self.animating = False
    # ADD INTERACT ANIMATION AND PLANT COLLECTION COUNTER 
    # AND MAKE PLANTS RUN OUT OF STUFF
    # update function
    def update(self, dt, tiles, objs):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles, objs)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, objs)
        self.checkInteraction(tiles, objs)
        if self.current_image != 0 and not self.animating:
                self.current_image = 0
        self.image = self.sprites[int(self.current_image)] 
    # check interaction function
    def checkInteraction(self, tiles, objs):
        objs = self.get_hits(tiles, objs)
        for obj in objs:
            # check obj hits and check if plant obj
            if type(obj) == PlantObject:
                # set interactable to true
                self.interactable = True
                self.interType = "plant"
            else:
                # else false so no perma interact
                self.interactable = False   
            if self.interactable:
                if self.interType == "plant":
                    if self.E_KEY:
                        # do plant interaction here
                        if obj.stock > 0:
                            obj.interact()
                            self.plantInteract()
                        else:
                            print("Out of stock")
                        print(obj.stock)
                        self.E_KEY = False
                        self.interactable = False
    # horizontal movement with accel
    def horizontal_movement(self,dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= self.speed
            # animation
            self.anim_run()
        elif self.RIGHT_KEY:
            self.acceleration.x += self.speed
            # animation
            self.anim_run()
        elif not self.UP_KEY and not self.DOWN_KEY:
            # stop animation if no horizontal movement or vertical movement
            self.anim_stop()        
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x
    # vertical movement with accel
    def vertical_movement(self,dt):
        self.acceleration.y = 0
        if self.UP_KEY:
            self.acceleration.y -= self.speed
            # animation
            self.anim_run()
        elif self.DOWN_KEY:
            self.acceleration.y += self.speed
            # animation
            self.anim_run()
        elif not self.LEFT_KEY and not self.RIGHT_KEY:
            # stop animation if not vertical or horizontal movement
            self.anim_stop()
        # accel and velocity math
        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(4)
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.y = self.position.y
    # velocity limiter
    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0
        self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
        if abs(self.velocity.y) < .01: self.velocity.y = 0
    # checking for obj and tile hits
    def get_hits(self, tiles, objs):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                if tile.collidable:
                    hits.append(tile)
        for obj in objs:
            if self.rect.colliderect(obj):
                if obj.interactable:
                    hits.append(obj)           
        return hits
    # checking collisions and doing them
    def checkCollisionsx(self, tiles, objs):
        collisions = self.get_hits(tiles, objs)
        for tile in collisions:
            if type(tile) == Tile:
                if self.velocity.x > 0:  # Hit tile moving right
                    self.position.x = tile.rect.left - self.rect.w
                    self.rect.x = self.position.x
                elif self.velocity.x < 0:  # Hit tile moving left
                    self.position.x = tile.rect.right
                    self.rect.x = self.position.x
    # checking collisions and doing them
    def checkCollisionsy(self, tiles, objs):
        collisions = self.get_hits(tiles, objs)
        for tile in collisions:
            if type(tile) == Tile:
                if self.velocity.y > 0:  # Hit tile moving right
                    self.position.y = tile.rect.top - self.rect.h
                    self.rect.y = self.position.y
                elif self.velocity.y < 0:  # Hit tile moving left
                    self.position.y = tile.rect.bottom
                    self.rect.y = self.position.y