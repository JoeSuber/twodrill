import shelve
import pygame
from operator import itemgetter
from constants import win_width, win_height, green, yellow, black, maximum_high_scores

test_name = "QB"
test_score = 0

def sorted_high_scores():
    
    scores = shelve.open('scores')
    sorted_scores = sorted(scores.items(), key=itemgetter(1), reverse=True)
    scores.close()
    
    return sorted_scores


def add_a_score(player_name=test_name, score=test_score):
    scores = shelve.open('scores')
    scores[player_name] = score
    scores.close()

def get_player(screen=None):
    pass
    
def check_score(score=test_score):
    sorted_scores = sorted_high_scores()
    # fill up list if empty
    if len(sorted_scores) < maximum_high_scores:
        add_a_score(player_name=test_name+str(len(sorted_scores)+1), score=0)
        check_score(score=0)
        
    for place, old_high_score in enumerate(sorted_scores):
        if (score > old_high_score[1]) and (place < maximum_high_scores):
            print(f"{score} is the #{place+1}th score")
            return "ENTER YOUR NAME, CHAMP!", place + 1
    
    return f"LAST QB: {score}", 0

def render_scores(sorted_scores, score_screen=None)
    line_spacer = 50
    if score_screen is None:
        pygame.init()
        score_screen = pygame.display.set_mode((win_width, win_height))
    score_font = pygame.font.Font('blubfont.ttf', 50)
    renders,rects = {}, {}
    for num, score in enumerate(sorted_scores):
        place = str(num +1)
        name = score[0]
        digits = str(score[1].rjust(3, "0"))
        place_ren = score_font.render(place, True, yellow, black)
        name_ren = score_font.render(name, True, green, black)
        score_ren = score_font.render(digits, True, green, black)
        wdth, _ = score_font.size(name)
        place_rect = place_ren.get_rect()
        name_rect = name_ren.get_rect()
        score_rect = score_ren.get_rect()
        place_rect.center = (win_width - int(win_width * 0.3), win_height - int(win_height * 0.9) + (line_spacer*num))
        name_rect.center = (win_width - int(win_width * 0.4), win_height - int(win_height * 0.9) + (line_spacer*num))
        score_rect.center = (win_width - int(win_width * 0.8) + (wdth // 2), win_height - int(win_height * 0.9) + (line_spacer*num))
        renders[num+1] = (place_ren, name_ren, score_ren)
        rects[num+1] = (place_rect, name_rect, score_rect)
        if (num+1) > maximum_high_scores:
            break
        
    return renders, rects

    
if __name__ == "__main__":
    scoreit()
    pygame.quit()
    