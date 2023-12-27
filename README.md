# twodrill
arcade football toss game with scoreboard

to start the game, run idlescreen.py from the command line:
"python3 idlescreen.py"

to exit game, press mouse button

to change music and sounds, put samples in the various "sound" dirs

the "good" are sensors for target holes A,B,C1, and C2

the "bad" events are interceptions on IN1, IN2, IN3

music and sounds are chosen randomly from the categories

*current system setup notes*

Raspberry Pi 4 w raspbian 64 bit OS
sensors are switches and IR sensors with signal pulled high

start_button = [board.D26]
pinlist = [board.D20, board.D23, board.D17, board.D27, board.D25, board.D13, board.D18]
sensor_names = ["A", "B", "C1", "C2", "IN1", "IN2", "IN3"]
point_list = [21, 7, 3, 3, 0, -2, -6]   # '0' is a time penalty
time_penalty = 10  #seconds

git remote set-url origin https://joesuber:<token>@github.com/joesuber/twodrill
https://raspberrypi.stackexchange.com/questions/98944/launch-a-gui-tkinter-program-on-boot
sudo chmod a+x start.sh

gotta do  this:
pip3 install RPI.GPIO
pip3 install adafruit-blinka
pip3 install adafruit-io
