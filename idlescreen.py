import time
import pygame
import board
import digitalio
import breakbeam
from highscore import check_score, add_a_score, render_scores, sorted_high_scores
from constants import *

start_message = "PRESS START"
last_score = 0
score_message = "LAST QUARTERBACK: 0"
all_time_text = "ALL TIME HIGHS:"
pinlist = [board.D24]
sensor_names = ["P1"]

all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP

pygame.init()
#screen = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
screen = pygame.display.set_mode((win_width, win_height))

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

sorted_scores = sorted_high_scores()

player_rens, player_rects = render_scores(sorted_scores, score_screen=screen)

action_flag, running = False, True
right_now = time.time()
last_hit = right_now
text_entry_timer = right_now
floater = 4
name_entry = ""
player_placed = 0

while running:
    # check sensors and buttons
    if not action_flag:
        for sensor_name, sensor in all_sensors.items():
            if (not sensor.value):
                last_hit = time.time()
                action_flag = True
                #start the game
                last_score = breakbeam.beamer(surface=screen, play_time=20)
                score_message, player_placed = check_score(score=last_score)
                if player_placed:
                    text_entry_timer = time.time() + text_time_delay
                    name_entry = ""
                score_ren = score_font.render(score_message, True, green, black)
                score_rect = score_ren.get_rect()
                score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))
                break
    
    # some sensor in the bunch recently triggered
    if action_flag and (right_now > (last_hit + cutout_interval)):
        action_flag = False
    
    # pygame event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                name_entry = name_entry[:-1]
                print(name_entry)
            elif event.key == pygame.K_RETURN and player_placed:
                print("RETURN hit")
                player_placed = 0
                add_a_score(player_name=name_entry, score=last_score)
                sorted_scores = sorted_high_scores()
                player_rens, player_rects = render_scores(sorted_scores, score_screen=screen)
                score_ren = score_font.render(f"WELL DONE {name_entry}!", True, green, black)
                score_rect = score_ren.get_rect()
                score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))   
                name_entry = ""
            else:
                name_entry += event.unicode
                print(name_entry)
                
    start_rect.center = (start_rect.center[0], int(start_rect.center[1] + floater))
    if (start_rect.center[1] < int(win_height * 0.35)) or (start_rect.center[1] > int(win_height * 0.8)):
        floater = (floater * -1)
    
    screen.fill(black)
    for p, q in zip(player_rens.values(), player_rects.values()):
        for x in range(3):
            screen.blit(p[x], q[x])
    screen.blit(start_ren, start_rect)
    screen.blit(score_ren, score_rect)
    screen.blit(alltime_ren, alltime_rect)
    pygame.display.update()
    
    right_now = time.time() # must be last instruction in while-loop

pygame.quit()
        