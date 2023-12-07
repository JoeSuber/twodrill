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
start_rect.center = (win_width - int(win_width * 0.78), win_height - int(win_height * 0.5))

entry_rect = pygame.Rect(start_rect.x, start_rect.y, 737, 138)

score_ren = score_font.render(score_message, True, green, black)
score_rect = score_ren.get_rect()
score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))

alltime_ren = score_font.render(all_time_text, True, green, black)
alltime_rect = alltime_ren.get_rect()
alltime_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.91))

sorted_scores = sorted_high_scores()

player_rens, player_rects = render_scores(sorted_scores, score_screen=screen)

action_flag, running = False, True
congrats_sound = pygame.mixer.Sound(str(noise_dict["LOMBO"][0]))
right_now = time.time()
last_hit = right_now
text_entry_timer = right_now
floater = 4
name_entry = ""
player_placed = 0
play_music = True


while running:
    # check sensors and buttons
    if not action_flag:
        for sensor_name, sensor in all_sensors.items():  #really only looking for start button here
            if (not sensor.value):
                last_hit = time.time()
                action_flag = True
                #start the game
                last_score = breakbeam.beamer(surface=screen)
                pygame.mixer.music.fadeout(500)
                pygame.mixer.stop()
                play_music = True
                score_message, player_placed = check_score(score=last_score)
                if player_placed:
                    congrats_sound.play()
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
            elif ((event.key == pygame.K_RETURN) or (len(name_entry) > 20)) and player_placed:
                print("RETURN or max chars hit")
                pygame.mixer.music.fadeout(500)
                player_placed = 0
                add_a_score(player_name=name_entry, score=last_score)
                sorted_scores = sorted_high_scores()
                player_rens, player_rects = render_scores(sorted_scores, score_screen=screen)
                start_ren = togo_font.render(start_message, True, white, black)
                score_ren = score_font.render(f"WELL DONE {name_entry}!", True, green, black)
                score_rect = score_ren.get_rect()
                score_rect.center = (win_width - int(win_width * 0.5), win_height - int(win_height * 0.1))   
                name_entry = ""

            else:
                name_entry += event.unicode
                print(name_entry)
    
    if player_placed:
        blinker = "_" if (right_now < (int(right_now) + 0.5)) else " "
        start_ren = togo_font.render(name_entry + blinker, True, white, black)
    #    start_rect = start_ren.get_rect()
                                                        
    start_rect.center = (start_rect.center[0], int(start_rect.center[1] + floater))
    if (start_rect.center[1] < int(win_height * 0.20)) or (start_rect.center[1] > int(win_height * 0.79)):
        floater = (floater * -1)
    
    screen.fill(black)
    for p, q in zip(player_rens.values(), player_rects.values()):
        for x in range(3):
            screen.blit(p[x], q[x])
    entry_rect.y = start_rect.y-8
    entry_rect.x = start_rect.x-8
    entry_rect.w = 1800
    pygame.draw.rect(screen, (255,0,0), entry_rect, 10)
    screen.blit(start_ren, start_rect)
    screen.blit(score_ren, score_rect)
    screen.blit(alltime_ren, alltime_rect)
    pygame.display.update()
    
    if play_music:
        play_music = False
        pygame.mixer.music.load(str(noise_dict["ENTRY"][0]))
        pygame.mixer.music.play()
    right_now = time.time() # must be last instruction in while-loop

pygame.quit()
        