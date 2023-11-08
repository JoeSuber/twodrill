import time
import pygame
import board
import digitalio
import random
import breakbeam


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
start_message = "PRESS START TO PLAY"
last_high_score, all_time_score = 0, 0
score_message = f"LAST QB SCORED: {last_high_score}"
all_time_text = f"ALL TIME HIGH: {all_time_score}"
pinlist = [board.D24]
sensor_names = ["P1"]

all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP

pygame.init()
screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((win_width, win_height))

score_font = pygame.font.Font('blubfont.ttf', 100)
togo_font = pygame.font.Font('LiberationMono-Regular.ttf', 110)

start_ren = togo_font.render(start_message, True, white, black)
start_rect = start_ren.get_rect()
start_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.5))

score_ren = score_font.render(score_message, True, green, black)
score_rect = score_ren.get_rect()
score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))

alltime_ren = score_font.render(all_time_text, True, green, black)
alltime_rect = alltime_ren.get_rect()
alltime_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.91))

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
                last_high_score = breakbeam.beamer(surface=screen)
                score_message = f"LAST SCORE: {last_high_score}"
                score_ren = score_font.render(score_message, True, green, black)
                score_rect = score_ren.get_rect()
                score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))
                if last_high_score > all_time_score:
                    all_time_score = last_high_score
                    alltime_ren = score_font.render(f"ALL TIME HIGH: {all_time_score}", True, green, black)
                    alltime_rect = alltime_ren.get_rect()
                    alltime_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.91))
                start_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.5))
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
    screen.blit(score_ren, score_rect)
    screen.blit(alltime_ren, alltime_rect)
    pygame.display.update()
    
    right_now = time.time() # must be last instruction in while-loop

pygame.quit()
        