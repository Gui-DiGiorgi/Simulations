# In here, we have a microecosystem simulation, with food spawning and little squares eating it. Every block has their own color, this never changes,
# what changes however is the walking speed and energy efficiency when creating children. They can get faster or slower, it depends on what the environment calls for.
# The little block inside them indicates their energy supply, the whiter, the bigger. When they have too much energy, they create children. 
# They can also die of old age or hunger. If they die of hunger, they don't create a food corpse, but if they die of old age and still have good energy, 
# they leave a little food block behind.
# I leave to the person that run this code to see how the number of animals and food relates as time goes on.

import pygame
from pygametexting import pyg_text
import random
import time
import math

def sign(init,dest):
    if init>dest:
        return -1
    elif init<dest:
        return 1
    else:
        return 0
    
def raw_distance(x_init,y_init,x_dest,y_dest):
    return math.sqrt((x_dest-x_init)**2+(y_dest-y_init)**2)
    
sizes = 15

class animal():
    def __init__(self, color_symbol, time, death, x, y, w_destiny, energy, speed, eff):

        self.x = x
        self.y = y
        self.energy = energy
        self.init_energy = energy
        self.speed = speed
        self.eff = eff
        self.color_symbol = color_symbol
        self.size = sizes
        self.time = time
        self.death = death
        self.x_dest = w_destiny[0]
        self.y_dest = w_destiny[1]
        
    def looking_for_food(self,w_destiny):
        self.x_dest = w_destiny[0]
        self.y_dest = w_destiny[1]
        
    def running(self):
        
        add_x = sign(self.x,self.x_dest)*int(self.speed)
        add_y = sign(self.y,self.y_dest)*int(self.speed)
        
        self.x += add_x
        self.y += add_y
        
        self.energy -= (abs(add_x)+abs(add_y))/self.eff
        
    def reach_food(self,food_x,food_y):
        add_x = sign(self.x,food_x)*int(self.speed)
        add_y = sign(self.y,food_y)*int(self.speed)
        
        self.x += add_x
        self.y += add_y
        
        self.energy -= (abs(add_x)+abs(add_y))/self.eff
        
    def draw(self,window):
        true_hunger = round(255*self.energy/self.init_energy)
        
        if true_hunger>255:
            true_hunger = 255
            
        true_color = (true_hunger,true_hunger,true_hunger)
        
        self.color = (true_hunger,true_hunger,true_hunger)
        pygame.draw.rect(window,self.color_symbol,(self.x,self.y,self.size,self.size))
        pygame.draw.rect(window,true_color,(int(self.x+self.size/2),int(self.y+self.size/2),
                                              int(self.size/2),int(self.size/2)))
        
class food():
    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.color = (255,0,0)
        self.size = sizes/2
    
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.size,self.size))
        
pygame.init()

win=pygame.display.set_mode((500,500))

pygame.display.set_caption("Standard")

pygtxt=pyg_text(20,(255,255,255),"comicsansms",win)

clock = pygame.time.Clock()

clock_time = 60

animals = []

foodie = []

run = True

spot_range = 30
eat_range = 10

now = time.time()

init_animals = 20

init_food = 50

mutation = True

old_age = True

food_refil_speed = 0.5 # The lowest, the fastest, to the min 0

tick = 0

skills_legacy = [["Time","Current Highest Speed","Highest Speed",
                 "Current Highest Eff","Highest Eff"]]
population_legacy = [["Time","Animal Population", "Food Population"]]

highest_speed = 0
highest_eff = 0
c_highest_speed = 0
c_highest_eff = 0

speed_mut_values = list((round(0.01*x,2) for x in range(10,31)))
eff_mut_values = list((round(0.01*x,2) for x in range(10,21)))

for i in range(init_animals):
    speed = 0.1*random.randint(10,30)
    if speed>highest_speed:
        highest_speed = speed
    eff = 0.01*random.randint(80,99)
    if eff>highest_eff:
        highest_eff = eff
    unique_color = (random.randint(120,200),random.randint(120,200),random.randint(120,200))
    animals.append(animal(unique_color,time.time(),random.randint(20,31),random.randint(0,500),random.randint(0,500),
                          (random.randint(0,500),random.randint(0,500)),1000,speed,eff))
    
for i in range(init_food):
    foodie.append(food(random.randint(0,500),random.randint(0,500)))

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
    
    if time.time()-now>food_refil_speed:
        foodie.append(food(random.randint(0,500),random.randint(0,500)))
        now = time.time()
    
    for i in animals.copy():
        
        food_found = False
        
        for f in foodie:
            
            range_max = [i.x + spot_range,i.y + spot_range]
            range_min = [i.x - spot_range,i.y - spot_range]
            
            if range_min[0]<f.x<range_max[0] and range_min[1]<f.y<range_max[1]:
                i.reach_food(f.x,f.y)
                food_found = True
                break
                
        if not food_found:
            if raw_distance(i.x,i.y,i.x_dest,i.y_dest) <= 4:
                i.looking_for_food((random.randint(0,500),random.randint(0,500)))
            else:
                i.running()
            
        for f in foodie.copy():
            
            range_max = [i.x + eat_range,i.y + eat_range]
            range_min = [i.x - eat_range,i.y - eat_range]
            
            if range_min[0]<f.x<range_max[0] and range_min[1]<f.y<range_max[1]:
                foodie.remove(f)
                i.energy += 500
                
        if i.energy <=0:
            animals.remove(i)
        if i.energy >= 2000:
            i.energy -= 1000
            #if mutation: #Both speed and eff change
            #    speed_mutation = i.speed + random.randint(-1,1)*random.choice(speed_mut_values)
            #    eff_mutation = i.eff + random.randint(-1,1)*random.choice(eff_mut_values)
            if mutation:
                speed_mutation = i.speed + random.randint(-1,1)*random.choice(speed_mut_values)
                eff_mutation = i.eff + random.randint(-1,1)*random.choice(eff_mut_values)
            else:
                speed_mutation = i.speed
                eff_mutation = i.eff
            animals.append(animal(i.color_symbol,time.time(),i.death,i.x,i.y,
                                  (random.randint(0,500),random.randint(0,500)),1000,speed_mutation,eff_mutation))
            
            
        if old_age:
            if time.time()-i.time >= i.death:
                if i.energy>=500:
                    foodie.append(food(i.x,i.y))
                if i in animals:
                    animals.remove(i)
                
    c_highest_speed = 0
    c_highest_eff = 0
    
    for i in animals:

        if i.speed>c_highest_speed:
            c_highest_speed = i.speed
            if c_highest_speed>highest_speed:
                highest_speed = c_highest_speed
        if i.eff>c_highest_eff:
            c_highest_eff = i.eff
            if c_highest_eff>highest_eff:
                highest_eff = c_highest_eff
                
                
        i.draw(win)
        
    for i in foodie:
        i.draw(win)
        
    highests = [c_highest_speed,highest_speed,c_highest_eff,highest_eff]
    
    approx_highests = []
        
    for i in highests:
        approx_highests.append(round(i,2))
        
        
    highest = "C.H. and H. Speed: {0}/{1}\nC.H. and H. Eff: {2}/{3}".format(approx_highests[0],approx_highests[1],
                                                                            approx_highests[2],approx_highests[3])
    
    last_skill_legacy = skills_legacy[len(skills_legacy)-1][1:5]
    
    if approx_highests != last_skill_legacy:
        
        skills_legacy.append([tick,approx_highests[0],approx_highests[1],
                              approx_highests[2],approx_highests[3]])
    
    pop_numbers = "Animals: {0} Food:{1}".format(len(animals),len(foodie))
    
    last_population_legacy = population_legacy[len(population_legacy)-1][1:3]
    
    if [len(animals),len(foodie)] != last_population_legacy:
    
        population_legacy.append([tick,len(animals),len(foodie)])
    
    tick += 1
    
    pygtxt.screen_multtext_centerpos(highest,(True,250),50,30)
    pygtxt.screen_text_centerpos(pop_numbers,250,250)
    pygtxt.screen_text_limitpos("Ticks:{0}".format(tick),495,495)

    pygame.display.update()
        
pygame.quit()
    
