# In this code, I simulate how little blocks would go around if they couldn't touch each other.
# The way they work is that they decide where to go and walk there following a sin(x) function. If there's blocks in the way,
# they try to not touch them and then go back to where they were planning to go.
# The crowd that sometimes form if there are too many blocks is funny.

#walking

import pygame
from pygametexting import pyg_text
import math
import random
import copy

def seek_value_index(n,target_list):
    
    tl = target_list

    bi = 0
    ei = len(tl) - 1
    bv = tl[bi]
    ev = tl[ei]
    
    if n<bv or n>ev:
        return [None,None]

    values = [bi,ei]
    repeat_control = []

    while (True):

        if repeat_control == values:
            break
        else: 
            repeat_control = values.copy()

        ci = int((bi+ei)/2)
        cv = tl[ci]

        if cv>bv and cv<=n:
            bi = ci
            bv = tl[ci]
        if cv<ev and cv>=n:
            ei = ci
            ev = tl[ci]

        values = [bi,ei]
        
    return values

def raw_distance(x_init,y_init,x_dest,y_dest):
    
    return math.sqrt((x_dest-x_init)**2+(y_dest-y_init)**2)

def active_percent(x_dist,y_dist):
    
    if x_dist == 0:
        return [1,0]
    elif y_dist == 0:
        return [0,1]
    else:
        rel = x_dist/y_dist
        return [(math.cos(math.atan(rel))),(math.sin(math.atan(rel)))]

def sign(init,dest):
    if init>dest:
        return -1
    elif init<dest:
        return 1
    else:
        return 0

class block():
    def __init__(self, size, x, y, speed,fear_speed,block_id):

        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.fear_speed = fear_speed
        self.fear = False
        self.location_sector = 0
        self.block_id = block_id
        
    def Destiny(self,w_destiny):
        self.x_dest = w_destiny[0]
        self.y_dest = w_destiny[1]
        
        self.init_walk_distance = round(raw_distance(self.x, self.y, self.x_dest, self.y_dest))
        
        self.zigzag = round(self.init_walk_distance/75)
        
        self.d_angle = active_percent(self.x-self.x_dest,self.y-self.y_dest)
        
        self.ghost_x = self.x
        self.ghost_y = self.y
        
    def Back_on_Track(self):
        
        self.init_walk_distance = round(raw_distance(self.x, self.y, self.x_dest, self.y_dest))
        
        self.zigzag = round(self.init_walk_distance/75)
        
        self.d_angle = active_percent(self.x-self.x_dest,self.y-self.y_dest)
        
        self.ghost_x = self.x
        self.ghost_y = self.y
        
    def Walking(self):
        
        self.ghost_x += sign(self.ghost_x,self.x_dest)*self.speed
        self.ghost_y += sign(self.ghost_y,self.y_dest)*self.speed
        
        c_dist = round(raw_distance(self.ghost_x, self.ghost_y, self.x_dest, self.y_dest))
        
        rem_dist = (self.init_walk_distance-c_dist)/self.init_walk_distance
         
        rem_dist = min(max(rem_dist,0),1)
        
        sin_ang = math.pi*rem_dist
        
        div = round(10*math.sin(self.zigzag*sin_ang))
        
        self.x = self.ghost_x + round(self.d_angle[0]*div)
        self.y = self.ghost_y + round(self.d_angle[1]*div)

    def Away(self,target_x,target_y):
        
        if self.x-target_x == 0:
            self.x -= sign(self.y,target_y)*int(self.fear_speed)
            self.y -= sign(self.y,target_y)*int(self.fear_speed)
                
        elif self.y-target_y == 0:
            self.x -= sign(self.x,target_x)*int(self.fear_speed)
            self.y -= sign(self.x,target_x)*int(self.fear_speed)
                
        else:
            self.x -= sign(self.x,target_x)*int(self.fear_speed)
            self.y -= sign(self.y,target_y)*int(self.fear_speed)
            
        self.fear = True
        
    def Borders(self,limits):
        self.x = min(max(self.x,limits[0][0]),limits[1][0])
        self.y = min(max(self.y,limits[0][1]),limits[1][1])
        
    def draw(self,win):
        pygame.draw.rect(win,(255,255,255),(self.x-int(self.size/2),self.y-int(self.size/2),self.size,self.size))

        
        
pygame.init()

display_size = (1300,720)

win=pygame.display.set_mode(display_size)

pygame.display.set_caption("Standard")

pygtxt=pyg_text(20,(255,255,255),"comicsansms",win)

clock = pygame.time.Clock()

clock_time = 60

field = display_size

field_x_cut = 130
field_y_cut = 40

field_x = int(field[0]/field_x_cut)
field_y = int(field[1]/field_y_cut)

light_barrier_x = []
light_barrier_y = []

for i in range(field_x+1):
    light_barrier_x.append(i*field_x_cut)
for i in range(field_y+1):
    light_barrier_y.append(i*field_y_cut)
    
light_barrier = []

for i in range(field_x):
    for j in range(field_y):
        light_barrier.append(((i*field_x_cut,j*field_y_cut),((i+1)*field_x_cut,(j+1)*field_y_cut)))
        
friends = []
sacred_number = len(light_barrier_y)
process = [-sacred_number,0,sacred_number]
checks = [[-sacred_number,0],[0,sacred_number],[sacred_number,2*sacred_number]]

for i in range(len(light_barrier)):
    add_ons = []
    limits = (i//sacred_number)*sacred_number
    for j,c in zip(process,checks):
        if limits+c[0]<=(i-1+j)<limits+c[1]:
            add_ons.append(i-1+j)
        if limits+c[0]<=(i+j)<limits+c[1]:
            add_ons.append(i+j)
        if limits+c[0]<=(i+1+j)<limits+c[1]:
            add_ons.append(i+1+j)
    for k in add_ons.copy():
        if 0<=k<=(len(light_barrier)-1):
            pass
        else:
            add_ons.remove(k)
    add_ons = list(set(add_ons))
    friends.append([i,add_ons])
    
block_group = []

block_n = 100

for i in range(block_n):
    block_group.append(block(10,random.randint(0,display_size[0]),random.randint(0,display_size[1]),2,3,i))
    block_group[i].Destiny((random.randint(0,display_size[0]),random.randint(0,display_size[1])))
    
run = True    
 
while run:
    
    clock.tick(clock_time)
    
    keys = pygame.key.get_pressed()
            
    mouse = pygame.mouse.get_pressed()
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Quits
    if keys[pygame.K_ESCAPE]:
        run = False
    
    win.fill((0,0,0))
    
    previous_group = copy.deepcopy(block_group)
    
    participants = []

    for i in range(field_x*field_y):
        participants.append([])

    for p in block_group:
        x_value = p.x
        y_value = p.y
        ix = seek_value_index(x_value,light_barrier_x)
        iy = seek_value_index(y_value,light_barrier_y)
        full_index = ix[0]*(len(light_barrier_y)-1)+iy[1]-1
        p.location_sector = full_index

    for p in block_group:
        participants[p.location_sector].append([p.block_id,p.x,p.y])
    
    for p,z in zip(block_group,previous_group):
        
        all_zones = friends[p.location_sector][1]
        all_friends = []
        for j in all_zones:
            all_friends += participants[j]
    
        if raw_distance(p.x,p.y,p.x_dest,p.y_dest) <= 6:
            p.Destiny((random.randint(0,display_size[0]),random.randint(0,display_size[1])))
        else:
            p.fear = False
            for k in all_friends:
                if p.block_id != k[0]:
                    if raw_distance(p.x,p.y,k[1],k[2]) <= p.size*2:
                        p.Away(k[1],k[2])
                        
            if p.fear != z.fear:
                if p.fear == False:
                    p.Back_on_Track()
            else:
                if p.fear == False:
                    p.Walking()
                    
            p.Borders(((0,0),display_size))
        
        p.draw(win)
    
    pygame.display.update()
        
pygame.quit()
