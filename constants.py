#constants
import board
import digitalio
from pathlib import Path

cutout_interval = 0.1   #stop registering hits until this interval elapses
pinlist = [board.D20, board.D23, board.D17, board.D27, board.D25, board.D13, board.D18]
sensor_names = ["A", "B", "C1", "C2", "IN1", "IN2", "IN3"]
point_list = [21, 7, 3, 3, -2, -3, 0]   # '0' is a time penalty
time_penalty = 7  #seconds
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
yellow = (255, 255, 0)
win_width, win_height = 1920, 1080
starting_words = ["DOWN", "SET", "BLUE 82", "OMAHA", "HIKE!"]
maximum_high_scores = 15  #how many to keep and show
text_time_delay = 60

noise_dict = {x.name: list(Path(x).glob("*.wav")) for x in Path("sounds").iterdir()}

award_points = {nm:award for nm, award in zip(sensor_names, point_list)}

all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP
    
