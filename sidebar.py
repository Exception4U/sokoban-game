import pygame
import sokoban

class Sidebar(object):
    def __init__(self, font):
        self.image=sokoban.load_image('sidebar.png')
        self.surface=pygame.surface.Surface(self.image.get_size()).convert()
        self.surface.blit(self.image, (0,0))
        self.font=font
        self.level=0
        self.moves=0
        self.steps=0
        self.render()

    def render(self):
        if(self.level<0):
            self.level=0
        if(self.moves<0):
            self.moves=0
        if(self.steps<0):
            self.steps=0
        self.surface.blit(self.image,(0,0))
        self.surface.blit(self.font.render(str(self.level), True, (0,0,0)), (100,98))
        self.surface.blit(self.font.render(str(self.moves), True, (0,0,0)), (100, 133))
        self.surface.blit(self.font.render(str(self.steps), True, (0,0,0)), (100, 167))

    def change_level(self, level):
        self.level=level
        self.render()
        
    def change_moves(self, moves):
        self.moves=moves
        self.render()

    def change_steps(self, steps):
        self.steps=steps
        self.render()

    def quick_rendertime(self, time):
        font_surface=self.font.render(time, True, (0,0,0))
        w,h=self.surface.get_size()
        f_w,f_h=font_surface.get_size()
        self.surface.blit(self.image, (0,251), (0, 251, 160, 30))
        self.surface.blit(font_surface, ((w/2)-(f_w/2), 251))

    def draw(self, screen):
        screen.blit(self.surface, ((screen.get_size()[0]/4)*3,0))

