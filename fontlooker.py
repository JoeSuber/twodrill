import time
import pygame
import os

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)
win_width, win_height = 1920//2, 1080//2

pygame.init()
display_surface = pygame.display.set_mode((win_width, win_height))
display_surface.fill(black)
filenames = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames)
             in os.walk("/usr/share/fonts/truetype") for f in filenames if f.endswith(".ttf")]
for font in filenames:
    print(f"{font}")
    continue_flag = False
    font_size = 1
    last_time = 0.1
    interval = 0.05
    while not continue_flag:
        if time.time() > (last_time + interval):
            last_time = time.time()
            font_size += 1
            word_font = pygame.font.Font(font, font_size)
            render_phrase = word_font.render("SECONDS TO GO:", True, white, black)
            rect_phrase = render_phrase.get_rect()
            rect_phrase.center = (win_width // 2, win_height // 2)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            continue_flag = True
            time.sleep(1)
        if keys[pygame.K_DOWN]:
            break
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
        
        display_surface.fill(black)
        display_surface.blit(render_phrase, rect_phrase)
        pygame.display.update()
pygame.quit()
        