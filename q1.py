from random import randint
from random import random
from math import exp
from math import log
import pygame
import sys

switch_time = 0
frames_per_sec = 60 # 1 (fps) = 1 (sec)
block_size = (50, 50)
bs_size = (20, 20)
road_width = 10
window_size = ((block_size[0] * 10 + road_width * 9), (block_size[1] * 10 + road_width * 9))
unit = 590 / 25
algo = ['Best Effort', 'Entropy', 'Threshold', 'My Algo']
p_min = 15
entropy = 20

 
speed = 0.02 * unit * 10# km / sec
forward_prob = 1 / 2
uturn_prob = 1 / 16
left_prob = 7 / 32
right_prob = 7 / 32
transmission_power = 120 # dB
arrival_rate = 2 / 3600 # calls / sec
service_time = 3 * 60 # sec
freq_table = [i * 100 for i in range(1, 11)]
car_entering_rate = (1/12) * exp(-(1/12))


alice_blue = (240, 248, 255) # for bs
chartreuse1 = (127,255,0)
cadetblue1 = (152,245,255)
cyan2 = (0,238,238)
darkolivegreen1 = (202,255,112)
darkorchid = (153,50,204)
dodgerblue2 = (28,134,238)
firebrick2 = (238,44,44)
hotpink = (255,105,180)
lightsalmon3 = (205,129,98)
orangered1 = (255,69,0)
black = (0, 0, 0)
white = (255, 255, 255)

top_border_y = 0
left_border_x = 0
bottom_border_y = window_size[1]
right_border_x = block_size[0] * 10 + road_width * 9

color_arr = (chartreuse1, cadetblue1,cyan2, darkolivegreen1, darkorchid, dodgerblue2, firebrick2, hotpink, lightsalmon3, orangered1)
bs_arr = []
car_arr = []

clock = pygame.time.Clock()
pygame.init()
window = pygame.display.set_mode(window_size)

car_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
base_station_group = pygame.sprite.Group()
font = pygame.font.match_font('arial')


def calculate_receiving_power(fc, dis):
    return transmission_power - (32.45 + 20 * (log(fc, 10)) + 20 * (log(dis, 10)))

def set_base_station_and_block():
    for i in range(10):
        for j in range(10):
            obj = block(i, j)
            block_group.add(obj)
            rand = randint(1, 10)
            if rand == 1:
                index = randint(0, 9)
                obj = base_station(i, j, index)
                bs_arr.append(obj)
                base_station_group.add(obj)
                
def best_effort_find_the_base_station(car):
    max_receiving_power = -(sys.maxsize)
    max_index = -1
    for i, bs in enumerate(bs_arr):
        dis = ((bs.rect.centerx - car.rect.centerx) ** 2 + (bs.rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        receiving_power = calculate_receiving_power(bs.freq, dis_in_km)
        if receiving_power > max_receiving_power:
            max_index = i
            max_receiving_power = receiving_power
            
    car.color = bs_arr[max_index].color
    car.received_power = round(max_receiving_power, 2)
    car.connected_bs = max_index
    
def entropy_find_the_base_station(car):
    max_receiving_power = -(sys.maxsize)
    max_index = -1
    for i, bs in enumerate(bs_arr):
        dis = ((bs.rect.centerx - car.rect.centerx) ** 2 + (bs.rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        receiving_power = calculate_receiving_power(bs.freq, dis_in_km)
        if receiving_power > max_receiving_power:
            max_index = i
            max_receiving_power = receiving_power
    # calculate current receiving power
    if car.connected_bs != -1:    
        dis = ((bs_arr[car.connected_bs].rect.centerx - car.rect.centerx) ** 2 + (bs_arr[car.connected_bs].rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        car.received_power = calculate_receiving_power(bs_arr[car.connected_bs].freq, dis_in_km)
        car.received_power = round(car.received_power, 2)
        
    if (max_receiving_power - car.received_power) > entropy:
        car.color = bs_arr[max_index].color
        car.received_power = round(max_receiving_power, 2)
        car.connected_bs = max_index

def threshold_find_the_base_station(car):
    if car.connected_bs != -1:    
        dis = ((bs_arr[car.connected_bs].rect.centerx - car.rect.centerx) ** 2 + (bs_arr[car.connected_bs].rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        car.received_power = calculate_receiving_power(bs_arr[car.connected_bs].freq, dis_in_km)
        car.received_power = round(car.received_power, 2)
        if car.received_power > p_min :
            return
        
    max_receiving_power = -(sys.maxsize)
    max_index = -1
    for i, bs in enumerate(bs_arr):
        dis = ((bs.rect.centerx - car.rect.centerx) ** 2 + (bs.rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        receiving_power = calculate_receiving_power(bs.freq, dis_in_km)
        if receiving_power > max_receiving_power:
            max_index = i
            max_receiving_power = receiving_power
                
    car.color = bs_arr[max_index].color
    car.received_power = round(max_receiving_power, 2)
    car.connected_bs = max_index
    
def entropy_modified_find_the_base_station(car):  
    max_receiving_power = -(sys.maxsize)
    max_index = -1
    
    shortest_index = -1
    shortest_dis_in_km = sys.maxsize
    
    for i, bs in enumerate(bs_arr):
        dis = ((bs.rect.centerx - car.rect.centerx) ** 2 + (bs.rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        receiving_power = calculate_receiving_power(bs.freq, dis_in_km)
        if receiving_power > max_receiving_power:
            max_index = i
            max_receiving_power = receiving_power
        if shortest_dis_in_km > dis_in_km:
            shortest_index = i
            shortest_dis_in_km = dis_in_km
            shortest_receiving_power = receiving_power
    # calculate current receiving power
    if car.connected_bs != -1:    
        dis = ((bs_arr[car.connected_bs].rect.centerx - car.rect.centerx) ** 2 + (bs_arr[car.connected_bs].rect.centery - car.rect.centery) ** 2) ** 0.5
        dis_in_km = dis / unit
        car.received_power = calculate_receiving_power(bs_arr[car.connected_bs].freq, dis_in_km)
        car.received_power = round(car.received_power, 2)
        
    if (max_receiving_power - car.received_power) > entropy:
        if car.connected_bs == -1:
            car.color = bs_arr[max_index].color
            car.received_power = round(max_receiving_power, 2)
            car.connected_bs = max_index
        else: # find the nearest base station
            car.color = bs_arr[shortest_index].color
            car.received_power = round(shortest_receiving_power, 2)
            car.connected_bs = max_index  
            
def create_car(i, j):
    if i == 0:
        x, y = block_size[0] * j + road_width * (j - 1), bottom_border_y
    elif i == 1:
        x, y = left_border_x, block_size[1] * j + road_width * (j - 1)
    elif i == 2:
        x, y = block_size[0] * j + road_width * (j - 1), top_border_y
    elif i == 3:
        x, y = right_border_x, block_size[1] * j + road_width * (j - 1)
        
    obj = car(x, y, i)
    if algorithm_select == 1:
        best_effort_find_the_base_station(obj)
    elif algorithm_select == 2:
        entropy_find_the_base_station(obj)
    elif algorithm_select == 3:
        threshold_find_the_base_station(obj)
    elif algorithm_select == 4:
        entropy_modified_find_the_base_station(obj)
    car_arr.append(obj)
    car_group.add(obj)
        
                
def if_needed_creating_car():
    for i in range(4): # 4 dirs.
        for j in range(1, 10):
            rand = random() # rand a floating number between (0, 1)
            if rand <= car_entering_rate: # create cars
                create_car(i, j)

class block(pygame.sprite.Sprite):
    def __init__(self, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(block_size)
        self.image.fill(alice_blue)
        
        self.rect = self.image.get_rect()
        self.rect.x = (block_size[0] + road_width) * i
        self.rect.y = (block_size[1] + road_width) * j
        
    def update(self):
        return
    
class base_station(pygame.sprite.Sprite):
    def __init__(self, i, j, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(bs_size)
        self.color = color_arr[index]
        self.image.fill(color_arr[index])
        self.freq = freq_table[index]
        
        self.rect = self.image.get_rect()
        self.rect.x = (block_size[0] + road_width) * i + ((block_size[0] - bs_size[0]) / 2)
        self.rect.y = (block_size[1] + road_width) * j + ((block_size[1] - bs_size[1]) / 2)
        
        p = randint(1, 4)
        if p == 1:
            self.rect.y = (block_size[1] + road_width) * j + ((block_size[1] - bs_size[1]) / 2) - (unit * 0.1)
        elif p == 2:
            self.rect.x = (block_size[0] + road_width) * i + ((block_size[0] - bs_size[0]) / 2) + (unit * 0.1)
        elif p == 3:
            self.rect.y = (block_size[1] + road_width) * j + ((block_size[1] - bs_size[1]) / 2) + (unit * 0.1)
        else:
            self.rect.x = (block_size[0] + road_width) * i + ((block_size[0] - bs_size[0]) / 2) - (unit * 0.1)
            
    def update(self):
        return

class car(pygame.sprite.Sprite):
    def __init__(self, x, y, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((road_width,road_width))
        self.connected_bs = -1
        self.color = white
        self.image.fill(self.color)
        self.rect = self.image.get_rect()  
        self.position_x = float(x)         
        self.position_y = float(y)
        self.rect.x = x    
        self.rect.y = y
        self.dir = dir 
        self.received_power = -(sys.maxsize)  
        
    def occur_intersection_check(self):
        x, y = self.rect.x, self.rect.y
        for i in range(9):
            for j in range(9):
                if x == (block_size[0] + (block_size[0] + road_width) * i) and y == (block_size[0] + (block_size[0] + road_width) * j):
                    return True
        return False
    
    def move_car(self):
        if self.dir == 0:
            self.position_y -= speed
        elif self.dir == 1:
            self.position_x += speed
        elif self.dir == 2:
            self.position_y += speed
        else:
            self.position_x -= speed
        
        self.rect.x = round(self.position_x)
        self.rect.y = round(self.position_y)
        
    def update(self):
        if self.occur_intersection_check():
            rand = randint(1, 32)
            if 17 <= rand and rand <= 18:
                self.dir += 2
            elif 19 <= rand and rand <= 25:
                self.dir += 1
            elif rand > 25:
                self.dir += 3
        self.dir %= 4
        self.move_car()    
        self.image.fill(self.color)   
        return 

def check_if_any_car_needs_to_be_removed():
    for car in car_arr:
        rect = car.rect
        if rect.left > right_border_x or rect.right < left_border_x or rect.top > bottom_border_y or rect.bottom < top_border_y:
            car.kill()
            car_arr.remove(car)
            
def display_bs_carrier_freq():
    for bs in bs_arr:
        carrier_freq = str(bs.freq) + ' MHz'
        bs_font = pygame.font.Font(font, 12)
        text = bs_font.render(carrier_freq, True, black)
        rect = text.get_rect()
        rect.centerx = bs.rect.centerx
        rect.centery = bs.rect.centery
        window.blit(text, rect)
        
def calculate_switch_times_and_draw_line(algorithm_select):
    for i, car in enumerate(car_arr):
        old_bs = car.connected_bs
        if algorithm_select == 1:
            best_effort_find_the_base_station(car)
        elif algorithm_select == 2:
            entropy_find_the_base_station(car)
        elif algorithm_select == 3:
            threshold_find_the_base_station(car)
        elif algorithm_select == 4:
            entropy_modified_find_the_base_station(car)
        received_power = str(car.received_power) + ' dB'
        pygame.draw.line(window , car.color, (bs_arr[car.connected_bs].rect.centerx, bs_arr[car.connected_bs].rect.centery), (car.rect.centerx, car.rect.centery), 1)
        car_font = pygame.font.Font(font, 14)
        text = car_font.render(received_power, True, car.color)
        rect = text.get_rect()
        rect.centerx = car.rect.x+10
        rect.centery = car.rect.y-10
        window.blit(text, rect)
        if car.connected_bs != old_bs:
            global switch_time
            switch_time += 1
    
        
def update(algorithm_select):
    check_if_any_car_needs_to_be_removed()
    display_bs_carrier_freq()
    calculate_switch_times_and_draw_line(algorithm_select)

def Restart():
    global switch_time
    switch_time = 0
    for car in car_arr:
        car.kill()
    car_arr.clear()
    
if __name__  == '__main__':
    algorithm_select = 1
    set_base_station_and_block()
    end_of_game = False
    while True:
        clock.tick(frames_per_sec)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_of_game = True
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_1):
                    Restart()
                    algorithm_select = 1
                elif(event.key == pygame.K_2):
                    Restart()
                    algorithm_select = 2
                elif(event.key == pygame.K_3):
                    Restart()
                    algorithm_select = 3
                elif(event.key == pygame.K_4):
                    Restart()
                    algorithm_select = 4
                
        if_needed_creating_car()
        
        window.fill(white)
        block_group.draw(window)
        base_station_group.draw(window)
        car_group.draw(window)

        block_group.update()
        base_station_group.update()
        car_group.update()
        update(algorithm_select)
        pygame.display.update()
        
        print("Switch times : {:d}, Car number : {:d}".format(switch_time, len(car_arr)))
        print("Algorithm : {}".format(algo[algorithm_select - 1]))
        if end_of_game:
            break
    pygame.quit()