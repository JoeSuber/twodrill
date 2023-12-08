# twodrill
arcade football toss game with scoreboard

if running for the first time, run: 
"python3 highscore.py"
 to create a clean scores.db

for production, comment out the escape key option in idlescreen.py
so that people can't accidentally leave the game.

to start the game, run idlescreen.py from the command line:
"python3 idlescreen.py"

to change music and sounds, put samples in the various "sound" dirs

the "good" are sensors for target holes A,B,C1, and C2

the "bad" events are interceptions on IN1, IN2, IN3

music and sounds are chosen randomly from the categories

*system setup notes*
Raspberry Pi 4 w raspbian 64 bit OS
sensors are switches and IR sensors with signal pulled high
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

gotta do  this:
pip3 install adafruit-io
