import pygame
from pygame.locals import *
from sokoban import load_image

class User(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.up=load_image('user_up.gif')
        self.down=load_image('user_down.gif')
        self.left=load_image('user_left.gif')
        self.right=load_image('user_right.gif')
        self.image=self.up
        self.rect = self.image.get_rect()
        self.direction = None
        self.tile_location = (0,0)

    def set_direction(self, direction):
        self.direction=direction
        if(direction[1]<0):
            self.image=self.up
        elif(direction[1]>0):
            self.image=self.down
        elif(direction[0]<0):
            self.image=self.left
        elif(direction[0]>0):
            self.image=self.right

    def set_location(self, location):
        self.rect[0]=location[0]*32 
        self.rect[1]=location[1]*32

    def update(self):
        return
