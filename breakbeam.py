import board
import digitalio
import time
import pprint
import pygame
import yell

cutout_interval = 0.1   #stop registering hits until this interval elapses
pinlist = [board.D20, board.D23, board.D17, board.D27]
sensor_names = ["A-A", "B_A", "C_A", "C_B"]
point_list = [7, 4, 2, 2]
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)
win_width, win_height = 1920, 1080

def beamer(surface=None):
    player_score = 0
    play_time = 12.0
    if surface is None:
        pygame.init()
        surface = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
    display_surface = surface
    yell.yella(surface=surface)
    pygame.display.set_caption('Scoreboard')
    togo_font = pygame.font.Font('LiberationMono-Regular.ttf', 110)
    timer_font = pygame.font.Font('blubfont.ttf', 430)
    
    score_font = pygame.font.Font('blubfont.ttf', 750)

    timer_renders = {num:timer_font.render(str(num), True, white, black) for num in range(121)}
    timer_rects = {name:text.get_rect() for name, text in timer_renders.items()}
    for rect in timer_rects.values():
        rect.center = (win_width - int(win_width/3.7), win_height - int(win_height / 5)) #position timer countdown

    render_togo = togo_font.render("SECONDS TO GO:", True, white, black)
    togo_rect = render_togo.get_rect()
    togo_rect.center = (win_width - int(win_width * 0.73), win_height - int(win_height * 0.22))

    render_home = togo_font.render("HOME:", True, white, black)
    home_rect = render_home.get_rect()
    home_rect.center = (win_width - int(win_width * 0.89), win_height - int(win_height * 0.7))

    digit_positions = {"dig1":0.69, "dig2":0.44, "dig3":0.19}
    score_renders, score_rects = {}, {}
    for slot, position in digit_positions.items():
        score_renders[slot] = {str(num):score_font.render(str(num), True, yellow, black) for num in range(10)}
        score_rects[slot] = {num:text.get_rect() for num, text in score_renders[slot].items()}
        for rect in score_rects[slot].values():
            rect.center = (win_width - int(win_width * position), int(win_height / 3.1))

    display_surface.fill(black)

    award_points = {nm:award for nm, award in zip(sensor_names, point_list)}
    all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
    for break_beam in all_sensors.values():
        break_beam.direction = digitalio.Direction.INPUT
        break_beam.pull = digitalio.Pull.UP
        
    tally_count = {name:0 for name in all_sensors.keys()}
    timestamp_hits = {name:[] for name in all_sensors.keys()}

    action_flag, running = False, True
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
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            running = False
            
        display_digit = int(end_time - right_now)
        display_score = str(player_score).rjust(3,"0")
        display_surface.fill(black)
        display_surface.blit(timer_renders[display_digit], timer_rects[display_digit])
        for digit, position in zip(display_score, digit_positions.keys()):
            display_surface.blit(score_renders[position][digit], score_rects[position][digit])
        display_surface.blit(render_togo, togo_rect)
        display_surface.blit(render_home, home_rect)
        pygame.display.update()
        
        right_now = time.time() # must be last instruction in while-loop

    # end while loop for throwing balls
    print("")        
    print("  ----------")        
    print(" GAME OVER ")
    print(f"total score = {display_score}")
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(timestamp_hits)
    
if __name__ == "__main__":
    beamer()
    pygame.quit()

