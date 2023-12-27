import shelve
import pygame
from operator import itemgetter
from constants import win_width, win_height, scaler, p_white, black, maximum_high_scores


def sorted_high_scores():
    localscores = {}
    with shelve.open('newscores') as scoredb:
        for x in range(maximum_high_scores):
            try:
                localscores[str(x+1)] = scoredb[str(x+1)]
            except KeyError:
                scoredb[str(x+1)] = ["", 0]
                localscores[str(x+1)] = scoredb[str(x+1)]
    
        sorted_scores = sorted(localscores.values(), key=itemgetter(1), reverse=True)
        scoredb.close()
    return sorted_scores


def add_a_score(player_name="", score=0):
    for place, oldscore in enumerate(sorted_high_scores()):
        if score > oldscore[1]:
            with shelve.open('newscores') as scoredb:
                templine = scoredb[str(place+1)]
                scoredb[str(place+1)] = [player_name, score]
                score = templine[1]
                player_name = templine[0]

    
def check_score(score=0):
    sorted_scores = sorted_high_scores()
        
    for place, old_high_score in enumerate(sorted_scores):
        if (score > old_high_score[1]) and (place < maximum_high_scores):
            print(f"{score} is the #{place+1}th score")
            return f"SCORE: {score} - ENTER YOUR NAME!", place + 1
    
    return f"LAST QB SCORED: {score}", 0


def kill_place(place):
    with shelve.open('newscores') as scoredb:
        badline = scoredb[str(place)]
        print(f"badline is {badline}")
        scoredb[str(place)] = ["DUDE!!!", badline[1]]
    with shelve.open('badwords') as profanity_db:
        profanity_db[badline[0]] = badline[1]
    return badline[0]

def fix_scores():
    change_count = 0
    bad_words = ["fuck", "shit", "asshole", "cunt", "bitch", "nigger", "tits", "pussy", "faggot"]
    with shelve.open("badwords") as profanity_db:
        for x in profanity_db.keys():
            bad_words.append(x)
    changes = {}
    with shelve.open("newscores") as scoredb:
        for rank, player_line in scoredb.items():
            checked = [bw in player_line[0] for bw in bad_words]
            if len(checked) and any(checked):
                changes[rank] = ["GO K-STATE!", player_line[1]]
                print(f"rank {rank} is {player_line}")
                print(f"list = {checked}")
                change_count += 1
        for change, line in changes.items():
            scoredb[change] = line
        
    print(f"changes = {change_count}")            
    return change_count

    
def render_scores(sorted_scores, score_screen=None):
    line_spacer = int(50*scaler)
    if score_screen is None:
        pygame.init()
        score_screen = pygame.display.set_mode((win_width, win_height))
    score_font = pygame.font.Font('blubfont.ttf', int(55*scaler))
    renders,rects = {}, {}
    for num, score in enumerate(sorted_scores):
        place = str(num +1)
        name = score[0]
        digits = str(score[1]).rjust(3, " ")
        place_ren = score_font.render(place, True, p_white, black)
        name_ren = score_font.render(name, True, p_white, black)
        score_ren = score_font.render(digits, True, p_white, black)
        ws, _ = score_font.size(digits)
        ns, _ = score_font.size(name)
        ps, _ = score_font.size(place)
        place_rect = place_ren.get_rect()
        name_rect = name_ren.get_rect()
        score_rect = score_ren.get_rect()
        place_rect.center = (win_width - int(win_width * 0.565) + (ps // 2), win_height - int(win_height * 0.83) + (line_spacer*num))
        name_rect.center = (win_width - int(win_width * 0.52) + (ns // 2), win_height - int(win_height * 0.83) + (line_spacer*num))
        score_rect.center = (win_width - int(win_width * 0.10) + (ws // 2), win_height - int(win_height * 0.83) + (line_spacer*num))
        renders[num+1] = (place_ren, name_ren, score_ren)
        rects[num+1] = (place_rect, name_rect, score_rect)
        if (num+1) >= maximum_high_scores:
            break
        
    return renders, rects

    
if __name__ == "__main__":
    add_a_score(player_name="Fake!", score=34)
    check_score(score=15)
    sorted_high_scores()
    pygame.quit()
    