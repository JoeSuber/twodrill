import time
import pygame
import os

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)
win_width, win_height = 1920, 1080
interval = 0.04  # seconds
grow_rate = 11    # in font size
max_size = 400   # also font size
font = "/home/clear/projects/hike/PibotoLtBoldItalic.ttf"
pygame.init()
#display_surface = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
display_surface = pygame.display.set_mode((win_width, win_height))
display_surface.fill(black)
starting_words = ["DOWN", "SET", "BLUE 82", "OMAHA", "HIKE!"]
for yell in starting_words:
    continue_flag = False
    font_size = 11
    last_time = 0.1
    while not continue_flag:
        if time.time() > (last_time + interval):
            last_time = time.time()
            font_size += (grow_rate + int(grow_rate*.5))
            word_font = pygame.font.Font(font, font_size)
            render_phrase = word_font.render(yell, True, (255, max(0, 255-int(font_size*0.6)), 0), black)
            rect_phrase = render_phrase.get_rect()
            rect_phrase.center = (win_width // 2, win_height // 2)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            continue_flag = True
            time.sleep(1)
        if keys[pygame.K_DOWN]:
            break
        if font_size > max_size:
            continue_flag = True
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                break
        display_surface.fill(black)
        display_surface.blit(render_phrase, rect_phrase)
        pygame.display.update()
pygame.quit()
        
        