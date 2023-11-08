import board
import digitalio
import time
import pprint
import pygame

pygame.init()
white = (255, 255, 255)
green = (40, 255, 40)
blue = (0, 0, 128)
black = (40, 40, 40)
yellow = (0, 128, 0)
win_width, win_height = 500, 275
display_surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Scoreboard')
timer_font = pygame.font.Font('blubfont.ttf', 96)
word_font = pygame.font.Font('blubfont.ttf', 172)
score_font = pygame.font.Font('blubfont.ttf', 250)
starting_words = ["Sehet", "Blue82", "Omaha", "Hike!"]
word_delay = 500

timer_renders = {num:timer_font.render(str(num), True, green, black) for num in range(121)}
timer_rects = {name:text.get_rect() for name, text in timer_renders.items()}
for rect in timer_rects.values():
    rect.center = (win_width - int(win_width/5), win_height // 2) #position timer countdown

for word in starting_words:
    timer_renders[word] = word_font.render(word, True, white, black)
    timer_renders[word] = timer_renders[word].get_rect()
    timer_rects[word].center = (win_width // 2, win_height // 2)   #position starting hike

digit_positions = [0.88, 0.64, 0.4]
score_renders = {num:score_font.render(str(num), True, yellow, black) for num in range(10)}
score_rect

display_surface.fill(black)

# must match order of pins to names
#pinlist = [board.D20, board.D21, board.D23, board.D24, board.D17, board.D27]
#sensor_names = ["A-A", "A_B", "B_A", "B_B", "C_A", "C_B"]
pinlist = [board.D20, board.D23, board.D17, board.D27, board.D24]
sensor_names = ["A-A", "B_A", "C_A", "C_B", "P1"]
point_list = [7, 4, 2, 2, 0]
award_points = {nm:award for nm, award in zip(sensor_names, point_list)}
all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}

for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP
    
tally_count = {name:0 for name in all_sensors.keys()}
timestamp_hits = {name:[] for name in all_sensors.keys()}

action_flag, running = False, True

#play_time = float(int(input("How many seconds to play? ")))
play_time = 20.0
player_score = 0
cutout_interval = 0.1   #stop registering hits until this interval elapses

right_now = time.time()
last_hit = right_now
end_time = right_now + play_time
print(f"starting experiment # {int(right_now)}")

# begin throwing balls
while (right_now < end_time) and running:
    # check sensors and buttons
    if not action_flag:
        for sensor_name, sensor in all_sensors.items():
            if (not sensor.value):
                tally_count[sensor_name] += 1
                player_score += award_points[sensor_name]
                print(f" {sensor_name} = {tally_count[sensor_name]}  - ", end="")
                last_hit = time.time()
                timestamp_hits[sensor_name].append(last_hit)
                action_flag = True
                break
    
    # some sensor in the bunch recently triggered
    if action_flag and (right_now > (last_hit + cutout_interval)):
        action_flag = False
    
    # pygame event loop
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
    
    display_digit = int(end_time - right_now)
    display_score = str(player_score).rjust(3,"0")
    display_surface.fill(black)
    display_surface.blit(text_objects[display_digit], text_rects[display_digit])
    for digit in display_score:
        display_surface.blit(text_objects[display_digit], 
        
    #display_surface.blit(text_objects[display_digit], text_rects[display_digit])
    pygame.display.update()
    
    right_now = time.time() # must be last instruction in while-loop

# end while loop for throwing balls
print("")        
print("  ----------")        
print(" GAME OVER ")
print(f"total score = {display_score}")
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(timestamp_hits)
pygame.quit()

