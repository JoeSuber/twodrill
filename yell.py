import time
import pygame
from constants import black, win_width, win_height, starting_words, noise_dict

def yella(surface=None):
    interval = 0.04  # seconds
    grow_rate = 11    # in font size
    max_size = 400   # also font size
    font = "PibotoLtBoldItalic.ttf"
    
    pygame.mixer.init()
    samples = [pygame.mixer.Sound(str(x)) for x in noise_dict["HIKE"]]
    pygame.mixer.music.fadeout(500)
    if surface is None:
        pygame.init()
        surface = pygame.display.set_mode((win_width, win_height))
    display_surface = surface
    display_surface.fill(black)
    for xq, yell in enumerate(starting_words):
        continue_flag = False
        font_size = 11
        last_time = 0.1
        if xq < len(samples):
            samples[xq].play()
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
            
    pygame.mixer.quit()
    
    return 0

if __name__ == "__main__":
    yella()
    pygame.quit()