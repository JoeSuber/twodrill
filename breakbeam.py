import board
import digitalio
import time
import pprint
import pygame

pygame.init()
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (60,60,60)
win_width, win_height = 500, 275
display_surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Scoreboard')
font = pygame.font.Font('freesansbold.ttf', 96)
wordfont = pygame.font.Font('freesansbold.ttf', 172)
starting_words = ["Sehet", "Blue82", "Omaha", "Hike!"]
text_objects = {num:font.render(str(num), True, green, black) for num in range(121)}
text_rects = {name:text.get_rect() for name, text in text_objects.items()}
for rect in text_rects.values():
    rect.center = (win_width - int(win_width/5), win_height // 2) #position timer countdown
for word in starting_words:
    text_objects[word] = wordfont.render(word, True, white, black)
    text_rects[word] = text_objects[word].get_rect()
    text_rects[word].center = (win_width // 2, win_height // 2)   #position starting hike

display_surface.fill(black)

# must match order of pins to names
#pinlist = [board.D20, board.D21, board.D23, board.D24, board.D17, board.D27]
#sensor_names = ["A-A", "A_B", "B_A", "B_B", "C_A", "C_B"]
pinlist = [board.D20, board.D23, board.D17, board.D27]
sensor_names = ["A-A", "B_A", "C_A", "C_B"]
point_list = [7, 4, 2, 2]
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
    
    # some sensor in the bunch triggered
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

    #for digit in display_score:
        
    #display_surface.blit(text_objects[display_digit], text_rects[display_digit])
    pygame.display.update()
    
    right_now = time.time() # must be last instruction in while-loop

# end while loop for throwing balls
print("")        
print("  ----------")        
print(" GAME OVER ")
print(f"total score = {display_score}")
#for sensor, hit_list in timestamp_hits.items():
#    if len(hit_list):
#        first = min(hit_list)
#        last = max(hit_list)
#        print(f"{sensor} sensor tripped for {last - first}")
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(timestamp_hits)
pygame.quit()

