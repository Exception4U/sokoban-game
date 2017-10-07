#!/usr/bin/env python
import pygame
from pygame.locals import *
import os
import sys
import user
import level
from sidebar import Sidebar
import time
import pickle

level_img=None
level_nums_img=None
font=None
user_sprite=None
level_obj=None

sliding_noise=None
hit_noise=None

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image.set_colorkey((255,255,255))
    return image

def display_level(screen, level):
    global level_img
    global level_nums_img
    if level_img is None:
        level_img = load_image("level.bmp")
    if level_nums_img is None:
        level_nums_img = load_image("numbers.bmp")
    to_display=str(level)
    level_img.set_colorkey(None)
    level_nums_img.set_colorkey(None)
    new_width=level_img.get_size()[0]+(len(to_display)*80)
    surface = pygame.Surface((new_width, 157))
    surface.blit(level_img,(0,0))
    cur_x=level_img.get_size()[0]
    for c in to_display:
        c_int = int(c)
        surface.blit(level_nums_img, (cur_x, 0), (c_int*80, 0, (c_int*80)+79, 157))
        cur_x+=80
    surface.set_colorkey((255,255,255))
    screen.blit(surface, ((screen.get_size()[0]/2)-(new_width/2), (screen.get_size()[1]/2)-(157/2)))
    
def get_text(text):
    global font
    retval=''
    screen=pygame.display.get_surface()
    surface=pygame.surface.Surface((480, 80))
    clock=pygame.time.Clock()
    w,h=screen.get_size()
    font_surface=font.render(retval, True, (0,0,0))
    prompt_surface=font.render(text, True, (0,0,0))
    surface.fill((128,128,128))
    surface.blit(prompt_surface, (10, 10))
    surface.fill((255,255,255), (10,40,460, 25))
    surface.blit(font_surface,(11,34),((font_surface.get_size()[0]>460) and (font_surface.get_size()[0]-460) or 0 , 0, font_surface.get_size()[0]+460, font_surface.get_size()[1]))
    screen.blit(surface, ((w/2)-240, (h/2)-40))
    pygame.display.flip()
    down_key=None
    down_this=False
    while True:
        down_this=False
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                down_key=event
                if down_key.key == K_BACKSPACE:
                    retval = retval[:-1]
                elif down_key.key == K_RETURN:
                    return retval
                elif down_key.key == K_ESCAPE:
                    return ''
                else:
                    retval += str(down_key.unicode)
                font_surface=font.render(retval, True, (0,0,0))
                surface.fill((255,255,255), (10,40,460, 25))
                surface.blit(font_surface,(11,34),((font_surface.get_size()[0]>460) and (font_surface.get_size()[0]-460) or 0 , 0, font_surface.get_size()[0]+460, font_surface.get_size()[1]))
                screen.blit(surface, ((w/2)-240, (h/2)-40))
                pygame.display.flip()
                down_this=True
            if event.type == KEYUP:
                down_key=None
            elif event.type == QUIT:
                sys.exit(0)
        if down_key is not None and not down_this:
            if down_key.key == K_BACKSPACE:
                retval = retval[:-1]
            else:
                retval += str(down_key.unicode)
            font_surface=font.render(retval, True, (0,0,0))
            font_surface=font.render(retval,True, (0,0,0))
            surface.fill((255,255,255), (10,40,460, 25))        
            surface.blit(font_surface,(11,34),((font_surface.get_size()[0]>460) and (font_surface.get_size()[0]-460) or 0 , 0, font_surface.get_size()[0]+460, font_surface.get_size()[1]))
            screen.blit(surface, ((w/2)-240, (h/2)-40))
            pygame.display.flip()
    return retval

def run_level(cur_level, allsprites, background, sidebar,clock):
    global user_sprite
    global level_obj
    global hit_noise
    global sliding_noise
    level_obj=level.Level(cur_level, user_sprite)
    screen=pygame.display.get_surface()
    direction=(0,0)
    down=0
    down_next=False
    level_x=level_obj.start_x
    level_y=level_obj.start_y
    coord_x=level_obj.coord_x
    coord_y=level_obj.coord_y
    undo=[]
    is_undo=False
    has_undone=False
    moves=0
    steps=0
    time_spent=0
    moved=False
    while True:
        clock.tick(5)
        if down_next:
            down=0
            down_next=False
        if down>=1:
            down+=1
        for event in pygame.event.get():
            if event.type == KEYUP:
                if(down>1):
                    down=0
                else:
                    down_next=True
            elif event.type == KEYDOWN:
                down=1
                if event.key == K_UP:
                    down_next=False
                    direction=(0,-1)
                elif event.key == K_DOWN:
                    down_next=False
                    direction=(0,1)
                elif event.key == K_RIGHT:
                    down_next=False
                    direction=(1,0)
                elif event.key == K_LEFT:
                    down_next=False
                    direction=(-1,0)
                elif event.key == K_l:
                    load_file=get_text("Where to load from:")
                    if(load_file!=''):
                        load_f=open(load_file)
                        unpickler=pickle.Unpickler(load_f)
                        level_obj.num=unpickler.load()
                        level_obj.ports_completed=unpickler.load()
                        level_obj.start_x=unpickler.load()
                        level_obj.start_y=unpickler.load()
                        level_obj.coord_x=unpickler.load()
                        level_obj.coord_y=unpickler.load()
                        level_obj.width=unpickler.load()
                        level_obj.height=unpickler.load()
                        level_obj.tile_width=unpickler.load()
                        level_obj.tile_height=unpickler.load()
                        level_x=unpickler.load()
                        level_y=unpickler.load()
                        coord_x=unpickler.load()
                        coord_y=unpickler.load()
                        moves=unpickler.load()
                        steps=unpickler.load()
                        time_spent=unpickler.load()
                        level_obj.data=unpickler.load()
                        level_obj.orig_data=unpickler.load()
                        level_obj.render()
                        down_next=True
                        direction=(0,0)
                        sidebar.moves=moves
                        sidebar.steps=steps
                        sidebar.render()
                        is_undo=True
                        load_f.close()
                elif event.key == K_s:
                    save_file=get_text("Where to save game:")
                    if(save_file!=''):
                        save_f=open(save_file, "wt")
                        save_pickler=pickle.Pickler(save_f)
                        save_pickler.dump(level_obj.num)
                        save_pickler.dump(level_obj.ports_completed)
                        save_pickler.dump(level_obj.start_x)
                        save_pickler.dump(level_obj.start_y)
                        save_pickler.dump(level_obj.coord_x)
                        save_pickler.dump(level_obj.coord_y)
                        save_pickler.dump(level_obj.width)
                        save_pickler.dump(level_obj.height)
                        save_pickler.dump(level_obj.tile_width)
                        save_pickler.dump(level_obj.tile_height)
                        save_pickler.dump(level_x)
                        save_pickler.dump(level_y)
                        save_pickler.dump(coord_x)
                        save_pickler.dump(coord_y)
                        save_pickler.dump(moves)
                        save_pickler.dump(steps)
                        save_pickler.dump(time_spent)
                        save_pickler.dump(level_obj.data)
                        save_pickler.dump(level_obj.orig_data)
                        save_f.close()
                    moved=False
                    direction=(0,0)
                elif event.key == K_r:
                    level_obj.reset()
                    level_x=level_obj.start_x
                    level_y=level_obj.start_y
                    coord_x=level_obj.coord_x
                    coord_y=level_obj.coord_y
                    down_next=True
                    direction=(0,0)
                    moves=0
                    steps=0
                    sidebar.moves=0
                    sidebar.steps=0
                    time_spent=0
                    sidebar.render()
                    is_undo=True
                elif event.key == K_z:
                    return level_obj.num
                elif event.key == K_q:
                    sys.exit(0)
                elif event.key == K_u:
                    try:
                        undo_dir=undo.pop(0)
                        direction=map(lambda x: -x, undo_dir[0:2])
                        if(len(undo_dir)>2):
                            moves-=1
                            level_obj.move(undo_dir[4],undo_dir[5], undo_dir[2], undo_dir[3])
                        is_undo=True
                        has_undone=True
                        steps-=1
                        sidebar.moves=moves
                        sidebar.steps=steps
                        sidebar.render()
                    except:
                        direction=(0,0)
                        is_undo=True
                        pass
            elif event.type == QUIT:
                sys.exit(0)
        old_level_x=level_x
        old_level_y=level_y
        if down>=1:
            if has_undone and not is_undo:
                undo=[]
                has_undone=False
            level_x+=direction[0]
            level_y+=direction[1]
            user_sprite.set_direction(direction)
            if is_undo:
                is_undo=False
            else:
                moved=True
                undo.insert(0, list(direction[0:2]))
        if level_x<0:
            level_x=0
        if level_y<0:
            level_y=0
        if level_x==level_obj.tile_width:
            level_x=level_obj.tile_width-1
        if level_y==level_obj.tile_height:
            level_y=level_obj.tile_height-1
        if not level_obj.can_go(level_x, level_y):
            if(level_obj.get(level_x, level_y)==level.BOX):
                undo[0].append(level_x)
                undo[0].append(level_y)
                undo[0].append(level_x+direction[0])
                undo[0].append(level_y+direction[1])
                if not level_obj.move(level_x,level_y, level_x+ direction[0]  , level_y+direction[1]):
                    hit_noise.play(0,100)
                    undo.pop(0)
                    level_x=old_level_x
                    level_y=old_level_y
                elif moved:
                    sliding_noise.play(0,200)
                    moves+=1
                    sidebar.change_moves(moves)
            else:
                hit_noise.play(0,100)
                undo.pop(0)
                level_x=old_level_x
                level_y=old_level_y
        elif moved:
            steps+=1
            sidebar.change_steps(steps)
        coord_x+=level_x-old_level_x
        coord_y+=level_y-old_level_y
        time_spent+=1
        allsprites.update()
        screen.blit(background, (0,0))
        sidebar.quick_rendertime(time.strftime("%M:%S",time.gmtime(time_spent/5)))
        sidebar.draw(screen)
        level_obj.draw(screen, coord_x, coord_y)
        allsprites.draw(screen)
        pygame.display.flip()
        moved=False
        if(level_obj.ports_completed==level_obj.port_count):
            return level_obj.num

def wait_for_press(clock):
    done=False
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(1)
            if event.type == KEYDOWN or event.type==MOUSEBUTTONDOWN:
                done=True
        if done:
            break

def main():
    global font
    global user_sprite
    global hit_noise
    global sliding_noise
    pygame.init()
    if pygame.font is None:
        print "No pygame font!"
        sys.exit(1)
    font=pygame.font.Font(os.path.join('data','Comic Sans MS'), 20)
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("PySokoban");
    
    sliding_noise=pygame.mixer.Sound(os.path.join('data','box_slide.wav'))
    hit_noise=pygame.mixer.Sound(os.path.join('data','hit.wav'))

    background = load_image('bg.png')
    
    logo = load_image("logo.bmp")
    logo_w, logo_h = logo.get_size()

#    screen.blit(background, (0,0))
    screen.fill((255,255,255))
    screen.blit(logo, ((screen.get_size()[0]/2)-(logo_w/2), (screen.get_size()[1]/2)-(logo_h/2)))
    pygame.display.flip()
    
    clock = pygame.time.Clock()

    wait_for_press(clock)
    
    sidebar = Sidebar(font)

    user_sprite=user.User()
    allsprites=pygame.sprite.RenderPlain((user_sprite))

    screen.fill((255,255,255))

    cur_level=1
    while(1):
        sidebar.level=cur_level
        sidebar.moves=0
        sidebar.steps=0
        sidebar.render()
        display_level(screen, cur_level)
        pygame.display.flip()
        wait_for_press(clock)
        
        screen.blit(background, (0,0))
        sidebar.draw(screen)
        pygame.display.flip()
        try:
            cur_level=run_level(cur_level,allsprites, background, sidebar, clock)
        except level.NoMoreLevels:
            break
        cur_level+=1
        
#    begin_level(1)

    return

if __name__=="__main__": main()
