import time
import pygame
import board
import digitalio
import breakbeam
import random

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)
win_width, win_height = 1920, 1080
interval = 0.04  # seconds
cutout_interval = 0.1   #stop registering hits until this interval elapses
grow_rate = 11    # in font size
max_size = 400   # also font size
score_font = "PibotoLtBoldItalic.ttf"
bulb_font = "blubfont.ttf"
start_message = "PRESS START TO BEGIN"
pinlist = [board.D24]
sensor_names = ["P1"]

all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP

pygame.init()
screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((win_width, win_height))

timer_font = pygame.font.Font('blubfont.ttf', 430)
togo_font = pygame.font.Font('LiberationMono-Regular.ttf', 110)
start_ren = togo_font.render(start_message, True, white, black)
start_rect = start_ren.get_rect()
start_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.22))

action_flag, running = False, True
right_now = time.time()
last_hit = right_now

while running:
    # check sensors and buttons
    if not action_flag:
        for sensor_name, sensor in all_sensors.items():
            if (not sensor.value):
                last_hit = time.time()
                action_flag = True
                breakbeam.beamer(surface=screen)
                break
    
    # some sensor in the bunch recently triggered
    if action_flag and (right_now > (last_hit + cutout_interval)):
        action_flag = False
    
    # pygame event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        running = False
    start_rect.center = (start_rect.center[0]+random.choice((-1,1)), start_rect.center[1]+random.choice((-1,1)))
    screen.fill(black)
    screen.blit(start_ren, start_rect)
    pygame.display.update()
    
    right_now = time.time() # must be last instruction in while-loop

pygame.quit()
        