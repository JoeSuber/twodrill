#constants
import board
import digitalio

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
starting_words = ["DOWN", "SET", "BLUE 82", "OMAHA", "HIKE!"]
maximum_high_scores = 20
text_time_delay = 60

award_points = {nm:award for nm, award in zip(sensor_names, point_list)}
all_sensors = {s_name:digitalio.DigitalInOut(pin) for s_name, pin in zip(sensor_names, pinlist)}
for break_beam in all_sensors.values():
    break_beam.direction = digitalio.Direction.INPUT
    break_beam.pull = digitalio.Pull.UP
    
