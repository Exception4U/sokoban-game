import pygame
from pygame.locals import *
from sokoban import *
import os

NO_BLOCK=0
BRICK=1
BOX=2
PORT=3
USER=4
OFF_CHART=5

brick=None
box=None
port=None
floor=None

class NoMoreLevels(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "No more levels!"

class BadLevelDesign(Exception):
    def __str__(self):
        return "More boxes than ports or vice versa!"

class Level(object):
    def __init__(self, num, user_sprite):
        global brick
        global box
        global port
        global floor
        if brick is None:
            brick=pygame.image.load(os.path.join('data','brick.gif'))
        if box is None:
            box=pygame.image.load(os.path.join('data','box.gif'))
        if port is None:
            port=pygame.image.load(os.path.join('data','port.gif'))
        if floor is None:
            floor=pygame.image.load(os.path.join('data','floor.gif'))
        try:
            self.img=pygame.image.load(os.path.join('data', 'levels','level'+str(num)+".gif"))
        except pygame.error:
            raise NoMoreLevels()
        self.surface=pygame.Surface(map(lambda x: x*32, self.img.get_size())).convert()
        self.surface.fill((254,254,254))
        self.surface.set_colorkey((254,254,254))
        w,h=self.img.get_size()
        self.box_count=0
        self.port_count=0
        self.ports_completed=0
        self.data=[]
        self.orig_data=[]
        cur=[]
        for y in range(0,h):
            for x in range(0,w):
                cur_n=NO_BLOCK
                r,g,b=self.img.get_at((x,y))[0:3]
                if(r==255 and g==0 and b==0):
                    cur_n=BRICK
                elif(r==0 and g==255 and b==0):
                    self.box_count+=1
                    cur_n=BOX
                elif(r==0 and g==0 and b==255):
                    self.port_count+=1
                    cur_n=PORT
                elif(r==255 and g==255 and b==0):
                    cur_n=USER
                elif(r==0 and g==0 and b==0):
                    cur_n=OFF_CHART
                cur.append(cur_n)
            self.data.append(cur)
            self.orig_data.append(list(cur))
            cur=[]

        if(self.box_count!=self.port_count):
            raise BadLevelDesign()

        self.width,self.height=self.surface.get_size()
        self.tile_width=w
        self.tile_height=h
        self.user_sprite=user_sprite
        self.num=num
        self.render()

    def render(self):
        user_sprite=self.user_sprite
        for y in range(0,self.tile_height):
            for x in range(0,self.tile_width):
                if(self.data[y][x]==BRICK):
                    self.surface.blit(brick, (x*32, y*32))
                elif(self.data[y][x]==BOX):
                    self.surface.blit(box, (x*32, y*32))
                elif(self.data[y][x]==PORT):
                    self.surface.blit(port, (x*32, y*32))
                elif(self.data[y][x]==USER):
                    self.start_x=x
                    self.start_y=y
                    self.coord_x=self.start_x-7
                    self.coord_y=self.start_y-7
                    user_sprite.set_location((7,7))
                    self.surface.blit(floor, (x*32, y*32))
                elif(self.data[y][x]==NO_BLOCK):
                    self.surface.blit(floor, (x*32, y*32))

    def get(self, x, y):
        return self.data[y][x]

    def can_go(self,x,y):
        if(self.data[y][x]==BRICK or self.data[y][x]==BOX or self.data[y][x]==OFF_CHART):
            return False
        return True

    def move(self, from_x, from_y, to_x, to_y):
        if(self.data[from_y][from_x]!=BOX):
            return False
        if not self.can_go(to_x, to_y):
            return False
        if(self.data[to_y][to_x]==PORT):
            self.ports_completed+=1
        self.data[from_y][from_x]=0
        self.data[to_y][to_x]=BOX
        if(self.orig_data[from_y][from_x]==PORT):
            self.ports_completed-=1 # a move from a port to a port doesn't complete anything
            self.data[from_y][from_x]=PORT # make sure it's still a port
            self.surface.blit(port, (from_x*32, from_y*32))
        else:
            self.surface.blit(floor, (from_x*32, from_y*32))
        self.surface.blit(box, (to_x*32, to_y*32))
        return True

    def draw(self, screen, x, y):
        screen.blit(self.surface,(0,0),(x*32,y*32,480,480))

    def reset(self):
        user_sprite=self.user_sprite
        self.ports_completed=0
        self.data=[]
        for y in range(0,self.tile_height):
            self.data.append(list(self.orig_data[y]))
        self.surface.fill((254,254,254))
        self.render()
        
