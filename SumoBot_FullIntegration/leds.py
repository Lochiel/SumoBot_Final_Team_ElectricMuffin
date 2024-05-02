from neopixel import NeoPixel
from machine import Pin
import constants

#Singles Pinout
jewel_pin = Pin(constants.PIN_NEOPIXEL_Jewel, Pin.OUT)
jewel = NeoPixel(jewel_pin, 7)

#Jewel Pinout
singles_pin = Pin(constants.PIN_NEOPIXEL_Singles, Pin.OUT)
singles = NeoPixel(singles_pin, 4)


## NeoPixel uses a RGB tuple to define colors. We can predfinee colors; max values are 255, 
# for this demonstration we are using a fraction of that
# COLOR = (RED, GREEN, BLUE)
RED = (10,0,0)   #JEWEL
GREEN = (0,10,0)
BLUE = (0,0,10)
PURPLE = (5,1,20)
ORANGE = (25,5,0)
PINK = (20,1,10)
YELLOW = (20,20,0)
color_list = [RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,PINK]

#COLOR = (GREEN, RED, BLUE)
RED2 = (0,20,0)   #singles 
ORANGE2 = (7,25,0)
YELLOW2 = (10,15,0)
GREEN2 = (10,0,0)
BLUE2 = (7,1,20) 
PURPLE2 = (0,15,50)
PINK2 = (0,25,30)
color_list2 = [RED2,ORANGE2,YELLOW2,GREEN2,BLUE2,PURPLE2,PINK2]

brightness = 25
delay = .25
redJewel = (brightness,0,0) 
red = (0,brightness,0) 
i = 0
_mode = 0


### Red Pattern ###
_jewel_position = 1
_singles_position = 0
_singles_direction = True

def RedPatternUpdateJewel():
    global _jewel_position
    jewel[_jewel_position] = (0,0,0)
    _jewel_position = _jewel_position + 1
    if (_jewel_position > len(jewel)-1):
        _jewel_position = 1
    jewel[_jewel_position] = redJewel
    jewel.write()

def RedPatternUpdateSingles():
    global _singles_position, _singles_direction
    singles[_singles_position] = (0,0,0)
    if _singles_direction:
        _singles_position = _singles_position + 1
    else:
        _singles_position = _singles_position - 1
    singles[_singles_position] = red
    # print(_singles_position)
    if (_singles_position == len(singles)-1) or (_singles_position == 0):
        _singles_direction = not _singles_direction
    singles.write()

def RedHeartBeatJewel():
    if jewel[0] is not redJewel:
        jewel[0] = redJewel
    else:
        jewel[0] = (0,0,0)
    jewel.write()

def RedPatternUpdate():
    RedPatternUpdateJewel()
    RedPatternUpdateSingles()

def RedPatternSetup():
    #RedPattern doesn't require setup
    pass


### RainbowPattern ###
def RainbowPatternSetup(neopixel: NeoPixel, colorlist):
    j = 0
    for i in range(len(neopixel)):
        if j > len(colorlist)-1:
            j=0
        neopixel[i] = colorlist[j]
        j += 1
    neopixel.write()

def NextColor2(current_color2, color_list2):
#   print(current_color2)
  for i in range(len(color_list2)):
    if i == len(color_list2)-1:
        return color_list2[0]
    elif color_list2[i] == current_color2:
        return color_list2[i+1]

def RunPattern(neopixel: NeoPixel, colorlist):
    for i in range(len(neopixel)):
        Target_color2 = NextColor2(neopixel[i], colorlist)
        # print(f"{i}: {Target_color2}")
        neopixel[i] = Target_color2
    neopixel.write()
     
    
def RainbowUpdate():
    RunPattern(jewel, color_list)
    RunPattern(singles, color_list2)

def RainbowSetup():
    RainbowPatternSetup(jewel,color_list)
    RainbowPatternSetup(singles,color_list2)

def mode(NewMode:int):
    #Check to see if Mode Changed
    #set Global Mode
    #call Mode Setup Function
    global _mode
    if NewMode == 1:
        RainbowSetup()
        _mode = 1
    elif NewMode == 2:
       RedPatternSetup()
       _mode = 2
    pass

def update():
    #Check current mode
    #call appropriate update function
    if _mode == 1:
        RainbowUpdate()
    if _mode == 2:
        RedPatternUpdate()

def heartbeat():
    if _mode == 2:
        RedHeartBeatJewel()