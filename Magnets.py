# In this project, I simulate the magnet self ordering inside a repeling cage. I can alter the repeling force and how many magnets it has.
# The configurations it comes up with are nice to look at.

import pygame
from pygametexting import pyg_text
from math import sqrt

def sign(x,y):
    if x>y:
        return 1
    if x<y:
        return -1
    else:
        return 0
    
def extremes(num,minimum,maximum):
    if num>=maximum:
        return maximum
    elif num<=minimum:
        return minimum
    else:
        return num
    

class magnets_wall():
    
    def __init__(self,x,y,radius):
        
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255,255,255)
        
    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)
        
class magnets():
    
    def __init__(self,x,y,accel_const,radius):
        
        self.x = x
        self.y = y
        self.speedx = 0
        self.speedy = 0
        self.radius = radius
        self.color = (255,255,0)
        self.accel_const = accel_const
        
    def draw(self,window):
        pygame.draw.circle(window,self.color,(self.x,self.y),self.radius)
        
    def force(self,origin):
        x_dist = (self.x-origin[0])
        y_dist = (self.y-origin[1])
        self.full_dist = sqrt(x_dist**2+y_dist**2)
        
        if self.full_dist != 0:
        
            accel_result = self.accel_const/(self.full_dist)**2
            self.speedx = round(self.speedx + (abs(x_dist)/self.full_dist)*sign(self.x,origin[0])*accel_result)
            self.speedy = round(self.speedy + (abs(y_dist)/self.full_dist)*sign(self.y,origin[1])*accel_result)
        
        else:
            pass

    def action(self):
        self.x = self.x + self.speedx
        self.y = self.y + self.speedy
        
        self.speedx = round(self.speedx*extremes((1-round(abs(self.speedx/5),2)),0,1))
        self.speedy = round(self.speedy*extremes((1-round(abs(self.speedy/5),2)),0,1))
        

        
walls = []
y=0
plan = [[0,0,0,1],[1,500,0,1],[0,500,1,-1],[1,0,1,1]]

wall_density = 10

for p in plan:
    for i in range(wall_density+1):
        no = p[1]*p[2]+p[3]*i*int(500/wall_density)
        hue = [p[1],p[1]]
        hue[p[0]] = no
        hue = tuple(hue)
        walls.append(hue)
        
fresh_walls = []

for i in walls:
    if i not in fresh_walls:
        fresh_walls.append(i)
        
fresh_walls.sort()

barrier = []

true_radius = 5

for i in fresh_walls:
    barrier.append(magnets_wall(i[0],i[1],true_radius*2))

pygame.init()

win=pygame.display.set_mode((500,500))

pygame.display.set_caption("Standard")

pygtxt=pyg_text(20,(255,255,255),"comicsansms",win)

clock = pygame.time.Clock()

clock_time = 60

blops = []

run = True

true_accel = 100*(10**3)

modify = False

while run:
    
    clock.tick(clock_time)
    
    keys = pygame.key.get_pressed()
            
    mouse = pygame.mouse.get_pressed()
    
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
                blops.append(magnets(mouse_pos[0],mouse_pos[1],true_accel,true_radius))
            
    keys = pygame.key.get_pressed()
            
    mouse = pygame.mouse.get_pressed()
    
    # Quits
    if keys[pygame.K_ESCAPE]:
        run = False
    
    win.fill((0,0,0))
    
    if mouse[2]:
        blops = []
        
    if keys[pygame.K_2]:
        pygame.time.delay(150)
        true_accel += 10*10**3
        
        modify = True
        
    if keys[pygame.K_1]:
        pygame.time.delay(150)
        true_accel -= 10*10**3
        
        modify = True
    
    if modify:
        
        true_accel = int(extremes(true_accel,0,500*10**3))
        
        for i in blops:
            i.accel_const = true_accel
        modify = False
        
    for b in blops:
        for i in barrier:
            b.force([i.x,i.y])
        for bb in blops:
            if b==bb:
                pass
            else:
                b.force([bb.x,bb.y]) 
        b.action()
        
    for i in barrier:
        i.draw(win)
    for b in blops:
        b.draw(win)
        
    pygtxt.screen_text_centerpos(int(true_accel/10**3),250,250, color = (0,255,255))
        
    pygame.display.update()
        
pygame.quit()
